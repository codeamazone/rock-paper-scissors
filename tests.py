import pytest
import game
from game import RockPaperScissors
from pathlib import Path


@pytest.fixture(scope='class', name='setup1')
def setup_unknown_player():
    """Instantiate RockPaperScissors class with name that is not in the rating.txt file"""
    return RockPaperScissors('myname')


@pytest.fixture(scope='class', name='setup2')
def setup_known_player():
    """Instantiate RockPaperScissors class with name that is in the rating.txt file"""
    return RockPaperScissors('Tim')


def test_start_outputs_name(capsys, setup2):
    setup2.start()
    out, err = capsys.readouterr()
    assert out == 'Hello, Tim\n'
    assert err == ''


class TestClassAssignmentsNewPlayer:
    """Test if all value are assigned correctly upon instantiating the game class
    with a new player that is not in the rating file"""

    def test_name_is_assigned(self, setup1):
        assert setup1.player == 'myname'

    def test_initial_score_is_0(self, setup1):
        assert setup1.score == 0

    def test_start_leaves_initial_score(self, setup1):
        setup1.start()
        assert setup1.score == 0


class TestStartAssignmentPlayerInRating:
    """Test if all values are assigned correctly upon instantiating the game class
    with a player that is already in the rating file"""

    def test_name_is_assigned(self, setup2):
        assert setup2.player == 'Tim'

    def test_start_sets_score_form_file(self, setup2):
        setup2.start()
        assert setup2.score == 350


@pytest.mark.xfail(reason='patched dir/file seems to not be used, needs to be fixed')
def test_start_reads_from_file(tmp_path, monkeypatch, setup2, capsys):
    test_ratings = 'Pete 150\nTim 800'
    d = tmp_path / 'testdir'
    d.mkdir()
    testfile = d / 'rating.txt'
    testfile.write_text(test_ratings)
    assert testfile.read_text() == 'Pete 150\nTim 800'
    monkeypatch.setenv(str(Path(__file__).parent), str(d))
    setup2.start()
    assert setup2.score == 800

    # testdir = tmpdir.mkdir('home')
    # test_file = testdir.join('rating.txt')
    # test_file.write('Pete 150\nTim 800')
    # print(game.os.path)
    # monkeypatch.setattr(game.os.path, 'expanduser',
    #                      lambda x: x.replace('~', str(testdir)))
    # assert test_file.read() == 'Pete 150\nTim 800'
    # setup2.start()
    # assert setup2.score == 800




@pytest.fixture(scope='module', params=['myname', 'Tim'])
def setup(request):
    return RockPaperScissors(request.param)


class TestSetOptions:
    """Test if options are set correctly by set_options method"""
    def test_no_input_sets_default_options(self, monkeypatch, setup):
        # Simulate the user entering nothing in the terminal:
        monkeypatch.setattr('builtins.input', lambda _: '')

        setup.set_options()
        assert setup.options == ('rock', 'paper', 'scissors')

    @pytest.mark.xfail(reason='Even number of options should not be allowed')
    def test_input_of_even_number_of_options(self, monkeypatch, setup):
        # Simulate the user input
        monkeypatch.setattr('builtins.input', lambda _: 'spider, elephant')

        setup.set_options()
        assert setup.options == ['spider', 'elephant']

    def test_input_of_odd_number_of_options(self, monkeypatch, setup):
        # Simulate the user input
        monkeypatch.setattr('builtins.input', lambda _: 'spider, elephant, dragon')

        setup.set_options()
        assert setup.options == ['spider', 'elephant', 'dragon']

    def test_input_without_spaces(self, monkeypatch, setup):
        mock_input = 'spider,elephant,dragon'
        monkeypatch.setattr('builtins.input', lambda _: mock_input)

        setup.set_options()
        assert setup.options == ['spider', 'elephant', 'dragon']

    @pytest.mark.xfail(reason='set_up method does not split at whitespaces')
    def test_input_without_commas(self, monkeypatch, setup):
        mock_input = 'spider elephant lobster'
        monkeypatch.setattr('builtins.input', lambda _: mock_input)

        setup.set_options()
        assert setup.options == ['spider', 'elephant', 'lobster']

    def test_input_of_integers_instead_of_strings(self, monkeypatch, setup):
        # Simulate the user input
        monkeypatch.setattr('builtins.input', lambda _: '1, 5, 8')

        setup.set_options()
        assert setup.options == ['1', '5', '8']

    @pytest.mark.xfail(reason='Options should be unique')
    def test_input_of_repeated_options(self, monkeypatch, setup):
        # Simulate the user input
        monkeypatch.setattr('builtins.input', lambda _: 'spider, spider, spider')

        setup.set_options()
        assert setup.options == ['spider', 'spider', 'spider']

    @pytest.mark.xfail(reason='Entering just one option should be impossible')
    def test_input_of_just_one_option(self, monkeypatch, setup):
        # Simulate the user input
        monkeypatch.setattr('builtins.input', lambda _: 'spider')

        setup.set_options()
        assert setup.options == ['spider']


@pytest.fixture(name='all_setup')
def set_up_class_with_all_values_set(monkeypatch, setup1):
    test_options = 'dragon, spider, shrimp'
    monkeypatch.setattr('builtins.input', lambda _: test_options)
    setup1.set_options()


@pytest.mark.usefixtures('all_setup')
class TestUpdateScore:
    def test_update_with_draw(self, setup1):
        outcome = 'There is a draw (shrimp)'
        setup1.update_score(outcome)
        assert setup1.score == 50

    def test_update_with_win(self, setup1):
        """Make sure 100 points are added to already set 50 points"""

        outcome = 'Well done. Computer chose spider and failed'
        setup1.update_score(outcome)
        assert setup1.score == 150

    def test_update_being_called_repeatedly(self, setup1):
        """Add 50 and then 100 points to the preset score resulting from previous test functions"""

        outcome1 = 'There is a draw (shrimp)'
        outcome2 = 'Well done. Computer chose spider and failed'
        outcome3 = 'Sorry, but computer chose dragon'
        setup1.update_score(outcome1)
        setup1.update_score(outcome2)
        setup1.update_score(outcome3)

        assert setup1.score == 300


@pytest.mark.usefixtures('all_setup')
class TestDetermineWinner:
    def test_winning_option_wins(self, setup1):
        choice1 = 'spider'
        choice2 = 'shrimp'
        setup1.determine_winner(choice1, choice2)
        assert setup1.outcome == f'Well done. Computer chose spider and failed'

    def test_losing_option_loses(self, setup1):
        choice1 = 'spider'
        choice2 = 'dragon'
        setup1.determine_winner(choice1, choice2)
        assert setup1.outcome == 'Sorry, but computer chose spider'

    def test_same_option_results_in_draw(self, setup1):
        choice1 = 'spider'
        choice2 = 'spider'
        setup1.determine_winner(choice1, choice2)
        assert setup1.outcome == 'There is a draw (spider)'


class TestPlayGame:
    pass