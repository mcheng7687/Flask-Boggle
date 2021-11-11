const timeEveryRound = 60;      //expressed in seconds
let timeLeft = timeEveryRound;  //expressed in seconds
let score = 0;                  //current score
const usedWords = [];           //array of words used

function start() {
    // Start function includes event listener for submitting words, 
    // getting current high score and starting timer

    $("#guess-word-form").on("submit", async function queryWord(evt) {
        evt.preventDefault();
        let query = $("#word").val();

        if (timeLeft >= 0) {

            $("#word").val("");

            if (!checkUsedWords(query)) {
                let response = await axios.post(`/test-word/${query}`);

                //console.log(response.data.result);
                //console.log(response.data.points);

                if (checkWord(response.data.result)) {
                    addPoints(response.data.points);
                    usedWords.push(query);
                    $("#used-words").html($("#used-words").html() + `<td>${query}<td>`);
                }
            }
        }
    });

    startTimer();
}

function startTimer() {
    // Start timer and display on DOM 
    $('#timer').text(timeLeft);
    timeLeft--;

    const timerInterval = setInterval(() => {

        $('#timer').text(timeLeft);

        if (timeLeft <= 0) {
            clearInterval(timerInterval);
            window.location.href=(`/game-over?score=${score}`)
        }

        timeLeft--;
    }, 1000);
}

function addPoints(value) {
    // Add value to current score
    score += value;
    $("#score-value").text(score);
}

function checkWord(response) {
    // Verify if word is valid 
    switch (response) {
        case 'ok':
            return true;
            break;
        case 'not-on-board':
        case 'not-word':
            return false;
            break;
    }
}

function checkUsedWords(wordInputted) {
    // Verify if inputted word was used previously. 
    //Compared inputted word to array of used words.
    for (let word of usedWords) {
        if (word == wordInputted)
            return true;
    }
    return false;
}

start();