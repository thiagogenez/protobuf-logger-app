from receiver_app_logger.logger import main


def test_main(capsys):  # `capsys` is a Pytest fixture that captures sys output.
    main()
    captured = capsys.readouterr()  # Capture the output of the `main` function.
    assert "Hello, World!" in captured.out  # Check if "Hello, World!" is in the output.
