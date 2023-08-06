import pytest
import yaml

import tuxrun.__main__
from tuxrun.__main__ import start, main


def touch(directory, name):
    f = directory / name
    f.touch()
    return f


@pytest.fixture
def device(tmp_path):
    return touch(tmp_path, "device.yaml")


@pytest.fixture
def job(tmp_path):
    return touch(tmp_path, "job.yaml")


@pytest.fixture
def run(mocker):
    return mocker.patch("tuxrun.__main__.run")


@pytest.fixture
def tuxrun_args(monkeypatch, device, job):
    args = ["tuxrun", "--device-dict", str(device), "--definition", str(job)]
    monkeypatch.setattr("sys.argv", args)
    return args


@pytest.fixture
def tuxrun_args_generate(monkeypatch):
    args = [
        "tuxrun",
        "--device",
        "qemu-i386",
        "--kernel",
        "https://storage.tuxboot.com/i386/bzImage",
    ]
    monkeypatch.setattr("sys.argv", args)
    return args


@pytest.fixture
def lava_run(mocker):
    Popen = mocker.patch("subprocess.Popen")
    proc = Popen.return_value
    proc.wait.return_value = 0
    proc.communicate.return_value = (mocker.MagicMock(), mocker.MagicMock())
    return proc


def test_start_calls_main(monkeypatch, mocker):
    monkeypatch.setattr(tuxrun.__main__, "__name__", "__main__")
    main = mocker.patch("tuxrun.__main__.main")
    with pytest.raises(SystemExit):
        start()
    main.assert_called()


def test_main_usage(monkeypatch, capsys):
    monkeypatch.setattr("tuxrun.__main__.sys.argv", ["tuxrun"])
    ret = main()
    assert ret != 0
    _, err = capsys.readouterr()
    assert "usage: tuxrun" in err


def test_almost_real_run(tuxrun_args, lava_run, capsys):
    lava_run.stderr = [
        '{"lvl": "info", "msg": "Hello, world", "dt": "2021-04-08T18:42:25.139513"}\n'
    ]
    exitcode = main()
    assert exitcode == 0
    stdout, _ = capsys.readouterr()
    assert "Hello, world" in stdout


@pytest.mark.parametrize(
    "argv",
    [
        [],
        ["--device", "qemu-armv7", "--device-dict", "device.yaml"],
        ["--device", "qemu-armv7", "--dtb", "bla.dtb"],
        ["--kernel", "https://storage.tuxboot.com/i386/bzImage"],
        ["--device-dict", "device.yaml"],
        ["--definition", "definition.yaml"],
    ],
)
def test_command_line_errors(argv, capsys, monkeypatch):
    monkeypatch.setattr("tuxrun.__main__.sys.argv", ["tuxrun"] + argv)
    exitcode = main()
    assert exitcode == 1
    stdout, stderr = capsys.readouterr()
    assert "usage: tuxrun" in stderr
    assert "tuxrun: error:" in stderr


def test_almost_real_run_generate(tuxrun_args_generate, lava_run, capsys):
    lava_run.stderr = [
        '{"lvl": "info", "msg": "Hello, world", "dt": "2021-04-08T18:42:25.139513"}\n'
    ]
    exitcode = main()
    assert exitcode == 0
    stdout, _ = capsys.readouterr()
    assert "Hello, world" in stdout


def test_ignores_empty_line_from_lava_run_stdout(tuxrun_args, lava_run):
    lava_run.stderr = [
        '{"lvl": "info", "msg": "Hello, world", "dt": "2021-04-08T18:42:25.139513"}\n',
        "",
        '{"lvl": "info", "msg": "Hello, world", "dt": "2021-04-08T18:42:26.139513"}\n',
    ]
    exitcode = main()
    assert exitcode == 0


def test_ignores_empty_line_from_lava_run_logfile(tuxrun_args, lava_run, tmp_path):
    log = tmp_path / "log.yaml"
    tuxrun_args += ["--log", str(log)]
    lava_run.stderr = [
        '{"lvl": "info", "msg": "Hello, world", "dt": "2021-04-08T18:42:25.139513"}\n',
        "",
        '{"lvl": "info", "msg": "Hello, world", "dt": "2021-04-08T18:42:26.139513"}\n',
    ]
    exitcode = main()
    assert exitcode == 0
    logdata = yaml.safe_load(log.open())
    assert type(logdata[0]) is dict
    assert type(logdata[1]) is dict


def test_tuxmake_directory(monkeypatch, tmp_path, run):
    tuxmake_build = tmp_path / "build"
    tuxmake_build.mkdir()
    (tuxmake_build / "metadata.json").write_text(
        """
        {
            "results": {
                "artifacts": {"kernel": ["bzImage"], "modules": ["modules.tar.xz"]}
            },
            "build": {"target_arch": "x86_64"}
        }
        """
    )
    monkeypatch.setattr("sys.argv", ["tuxrun", "--tuxmake", str(tuxmake_build)])

    main()
    run.assert_called()
    options = run.call_args[0][0]
    assert options.kernel == f"file://{tuxmake_build}/bzImage"
    assert options.device == "qemu-x86_64"


def test_no_modules(monkeypatch, tmp_path, run):
    tuxmake_build = tmp_path / "build"
    tuxmake_build.mkdir()
    (tuxmake_build / "metadata.json").write_text(
        """
        {
            "results": {
                "artifacts": {"kernel": ["bzImage"]}
            },
            "build": {"target_arch": "x86_64"}
        }
        """
    )
    monkeypatch.setattr("sys.argv", ["tuxrun", "--tuxmake", str(tuxmake_build)])

    main()
    run.assert_called()
    options = run.call_args[0][0]
    assert options.modules is None


def test_invalid_tuxmake_directory(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr("sys.argv", ["tuxrun", "--tuxmake", str(tmp_path)])
    with pytest.raises(SystemExit) as exit:
        main()
        assert exit.status_code != 0
    _, err = capsys.readouterr()
    assert "metadata.json" in err
