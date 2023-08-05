import justunits


def test_against_experiment():
    result = justunits.split_number_and_unit("Experiment")
    assert result == ('Experiment', ''), "Correct number split failed."

    result = justunits.split_attribute_unit("Experiment")
    assert result == ('Experiment', ''), "Correct attribute split failed."

    result = justunits.split_unit_text("Experiment")
    assert result == ('Experiment', ''), "Correct text split failed."