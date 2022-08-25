class Boggle{

    constructor(){
        this.seconds = 60
        this.score = 0
        this.words = []
        this.timer = setInterval(this.countDown.bind(this), 1000)

        $(".guess-form").on("submit", this.submitFunction.bind(this))
    }

    // Countdown
    async countDown() {
        this.seconds -= 1;
    
        this.updateTimer()
    
        if (this.seconds === 0) {
           clearInterval(this.timer);
           $("#guess-input").attr('disabled', 'disabled')
           $("#guess-submit-btn").attr('disabled', 'disabled')
           const response = await axios.post("/update", { score: this.score })
           $("#highest-score").text(response.data.highest)
           $('#played').text(response.data.nplay)
        }
    }
    
    // Submit the word and check its validity 
    async submitFunction(evt) {
        evt.preventDefault();
        const $guessInput = $("#guess-input")
        const $response = $("#response")
    
        const response = await axios.post("/check", {guess: $guessInput.val() })
        if (response.data.response == "not-word"){
            $response.html('<div class="alert alert-danger" role="alert">Not an English word!</div>')
        } else if (response.data.response == "not-on-board"){
            $response.html('<div class="alert alert-danger" role="alert">Word is not on the board!</div>')
        } else {
            if (this.words.includes($guessInput.val())){
                $response.html('<div class="alert alert-danger" role="alert">This word has already been guessed!</div>')
            } else {
                this.words.push($guessInput.val())
                this.score += $guessInput.val().length
                this.updateScore()
                $response.html('<div class="alert alert-success" role="alert">Word is on the board!</div>')
            }
        }
        $guessInput.val('')
        $guessInput.focus()
        
    }

    // Updates user's score
    updateScore(){
        const $score = $("#score")
        $score.text(this.score)
    }

    // Updates timer
    updateTimer(){
        const $timer = $("#timer")
        $timer.text(this.seconds)
    }
}


const boggle = new Boggle();