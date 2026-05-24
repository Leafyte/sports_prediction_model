/**
 * Sports Predictor Client-Side Application logic
 */

document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const tabButtons = document.querySelectorAll('.tab-btn');
    const sportInput = document.getElementById('sport-input');
    const formFields = document.querySelectorAll('.sport-form-fields');
    const predictionForm = document.getElementById('prediction-form');
    const predictSubmitBtn = document.getElementById('predict-submit-btn');
    
    // Result UI Elements
    const placeholderCard = document.getElementById('prediction-placeholder');
    const resultCard = document.getElementById('prediction-result-card');
    const resultSpinner = document.getElementById('result-spinner');
    const resultContent = document.getElementById('result-content');
    
    // Prediction Details Elements
    const resultWinnerTeam = document.getElementById('result-winner-team');
    const resultWinProb = document.getElementById('result-win-prob');
    const probRingIndicator = document.getElementById('prob-ring-indicator');
    const scoreTeam1Name = document.getElementById('score-team1-name');
    const scoreTeam2Name = document.getElementById('score-team2-name');
    const scoreTeam1Val = document.getElementById('score-team1-val');
    const scoreTeam2Val = document.getElementById('score-team2-val');
    const resultScoreText = document.getElementById('result-score-text');
    const resultModelName = document.getElementById('result-model-name');
    const resultModelAcc = document.getElementById('result-model-acc');
    const resultHistoryRows = document.getElementById('result-history-rows');

    // ==========================================
    // 1. SPORT TAB SELECTION
    // ==========================================
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const sport = button.getAttribute('data-sport');
            
            // Set active tab class
            tabButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            
            // Set sport in form input
            sportInput.value = sport;
            
            // Toggle form fields
            formFields.forEach(field => {
                if (field.id === `fields-${sport}`) {
                    field.classList.remove('hidden');
                } else {
                    field.classList.add('hidden');
                }
            });
            
            // Reset results display
            placeholderCard.classList.remove('hidden');
            resultCard.classList.add('hidden');
            
            // Re-validate the newly active form
            validateForm();
        });
    });

    // ==========================================
    // 2. SLIDER VALUE UPDATERS
    // ==========================================
    const sliders = [
        { id: 'fb-possession', outputId: 'fb-possession-val', suffix: '%' },
        { id: 'fb-shots', outputId: 'fb-shots-val', suffix: '' },
        { id: 'nba-rebounds', outputId: 'nba-rebounds-val', suffix: '' },
        { id: 'nba-assists', outputId: 'nba-assists-val', suffix: '' },
        { id: 'nba-shooting', outputId: 'nba-shooting-val', suffix: '%' }
    ];

    sliders.forEach(sliderInfo => {
        const slider = document.getElementById(sliderInfo.id);
        const output = document.getElementById(sliderInfo.outputId);
        if (slider && output) {
            slider.addEventListener('input', () => {
                output.textContent = `${slider.value}${sliderInfo.suffix}`;
            });
        }
    });

    // ==========================================
    // 3. TEAM SELECTORS DYNAMIC ACTIONS
    // ==========================================
    
    // Prevent selecting identical teams in dropdowns
    const selectElements = document.querySelectorAll('.team-select');
    selectElements.forEach(select => {
        select.addEventListener('change', () => {
            const container = select.closest('.sport-form-fields');
            const selects = container.querySelectorAll('.team-select');
            
            if (selects.length === 2) {
                const val1 = selects[0].value;
                const val2 = selects[1].value;
                
                // If same team selected, alert and reset the current one
                if (val1 && val2 && val1 === val2) {
                    alert("Please select two different teams.");
                    select.value = "";
                }
            }
            
            // Trigger specific sport loading actions
            const sport = sportInput.value;
            if (sport === 'ipl') {
                updateIplTossSelect();
                fetchSuggestedVenue();
            } else {
                fetchTeamHistoricalStats(sport);
            }
            
            validateForm();
        });
    });

    // IPL: Update Toss Winner choices dynamically based on Selected Teams
    function updateIplTossSelect() {
        const t1 = document.getElementById('ipl-team1').value;
        const t2 = document.getElementById('ipl-team2').value;
        const tossSelect = document.getElementById('ipl-toss');
        
        // Save current choice if applicable
        const currentChoice = tossSelect.value;
        
        // Reset options
        tossSelect.innerHTML = '<option value="" disabled selected>Choose Toss Winner</option>';
        
        if (t1 && t2) {
            const opt1 = document.createElement('option');
            opt1.value = t1;
            opt1.textContent = t1;
            tossSelect.appendChild(opt1);
            
            const opt2 = document.createElement('option');
            opt2.value = t2;
            opt2.textContent = t2;
            tossSelect.appendChild(opt2);
            
            // Restore choice if it matches new teams, otherwise default to team1
            if (currentChoice === t1 || currentChoice === t2) {
                tossSelect.value = currentChoice;
            } else {
                tossSelect.value = t1;
            }
            tossSelect.disabled = false;
        } else {
            tossSelect.disabled = true;
        }
    }

    // IPL: Fetch suggested venue based on Team 1's home venue
    function fetchSuggestedVenue() {
        const t1 = document.getElementById('ipl-team1').value;
        const t2 = document.getElementById('ipl-team2').value;
        const venueSelect = document.getElementById('ipl-venue');
        
        if (!t1 || !t2) return;
        
        fetch(`/api/team_stats?sport=ipl&team1=${encodeURIComponent(t1)}&team2=${encodeURIComponent(t2)}`)
            .then(res => res.json())
            .then(data => {
                if (data.suggested_venue) {
                    venueSelect.value = data.suggested_venue;
                }
            })
            .catch(err => console.error("Error fetching IPL venue:", err));
    }

    // Football & NBA: Load average statistics to prefill form sliders
    function fetchTeamHistoricalStats(sport) {
        let t1, t2, loadingBox;
        
        if (sport === 'football') {
            t1 = document.getElementById('fb-home').value;
            t2 = document.getElementById('fb-away').value;
            loadingBox = document.getElementById('fb-stats-loading-box');
        } else if (sport === 'nba') {
            t1 = document.getElementById('nba-home').value;
            t2 = document.getElementById('nba-away').value;
            loadingBox = document.getElementById('nba-stats-loading-box');
        }
        
        if (!t1 || !t2) return;
        
        // Show loading indicator
        loadingBox.classList.remove('hidden');
        
        fetch(`/api/team_stats?sport=${sport}&team1=${encodeURIComponent(t1)}&team2=${encodeURIComponent(t2)}`)
            .then(res => res.json())
            .then(data => {
                loadingBox.classList.add('hidden');
                
                if (sport === 'football' && data.possession && data.shots_on_target) {
                    // Update possession slider
                    const posSlider = document.getElementById('fb-possession');
                    const posVal = document.getElementById('fb-possession-val');
                    posSlider.value = data.possession;
                    posVal.textContent = `${data.possession}%`;
                    
                    // Update shots slider
                    const shotsSlider = document.getElementById('fb-shots');
                    const shotsVal = document.getElementById('fb-shots-val');
                    shotsSlider.value = Math.round(data.shots_on_target);
                    shotsVal.textContent = Math.round(data.shots_on_target);
                } 
                else if (sport === 'nba' && data.rebounds && data.assists && data.shooting_percentage) {
                    // Update rebounds slider
                    const rebSlider = document.getElementById('nba-rebounds');
                    const rebVal = document.getElementById('nba-rebounds-val');
                    rebSlider.value = data.rebounds;
                    rebVal.textContent = data.rebounds;
                    
                    // Update assists slider
                    const astSlider = document.getElementById('nba-assists');
                    const astVal = document.getElementById('nba-assists-val');
                    astSlider.value = data.assists;
                    astVal.textContent = data.assists;
                    
                    // Update shooting slider
                    const shtSlider = document.getElementById('nba-shooting');
                    const shtVal = document.getElementById('nba-shooting-val');
                    shtSlider.value = data.shooting_percentage;
                    shtVal.textContent = `${data.shooting_percentage}%`;
                }
            })
            .catch(err => {
                loadingBox.classList.add('hidden');
                console.error("Error preloading team statistics:", err);
            });
    }

    // ==========================================
    // 4. FORM VALIDATION CONTROL
    // ==========================================
    function validateForm() {
        const sport = sportInput.value;
        let isValid = false;
        
        if (sport === 'ipl') {
            const t1 = document.getElementById('ipl-team1').value;
            const t2 = document.getElementById('ipl-team2').value;
            const toss = document.getElementById('ipl-toss').value;
            isValid = (t1 && t2 && toss && t1 !== t2);
        } else if (sport === 'football') {
            const ht = document.getElementById('fb-home').value;
            const at = document.getElementById('fb-away').value;
            isValid = (ht && at && ht !== at);
        } else if (sport === 'nba') {
            const ht = document.getElementById('nba-home').value;
            const at = document.getElementById('nba-away').value;
            isValid = (ht && at && ht !== at);
        }
        
        predictSubmitBtn.disabled = !isValid;
    }

    // Bind validation on other inputs as well
    document.getElementById('ipl-toss').addEventListener('change', validateForm);

    // ==========================================
    // 5. RADIAL PROGRESS BAR HELPER
    // ==========================================
    function setRadialProbability(percent) {
        // SVG circle radius is 50. Circumference = 2 * PI * r = 2 * 3.14159 * 50 = 314.16
        const circumference = 314.16;
        probRingIndicator.style.strokeDasharray = `${circumference} ${circumference}`;
        
        // Calculate offset (percentage of circumference remaining)
        const offset = circumference - (percent / 100 * circumference);
        
        // Add style offset
        probRingIndicator.style.strokeDashoffset = offset;
    }

    // ==========================================
    // 6. ASYNC FORM SUBMISSION (INFERENCE API)
    // ==========================================
    predictionForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        const sport = sportInput.value;
        let payload = { sport };
        
        // Build payload based on sport
        if (sport === 'ipl') {
            payload.team1 = document.getElementById('ipl-team1').value;
            payload.team2 = document.getElementById('ipl-team2').value;
            payload.toss_winner = document.getElementById('ipl-toss').value;
            payload.toss_decision = document.getElementById('ipl-toss-decision').value;
            payload.venue = document.getElementById('ipl-venue').value;
        } else if (sport === 'football') {
            payload.home_team = document.getElementById('fb-home').value;
            payload.away_team = document.getElementById('fb-away').value;
            payload.possession = document.getElementById('fb-possession').value;
            payload.shots_on_target = document.getElementById('fb-shots').value;
        } else if (sport === 'nba') {
            payload.home_team = document.getElementById('nba-home').value;
            payload.away_team = document.getElementById('nba-away').value;
            payload.rebounds = document.getElementById('nba-rebounds').value;
            payload.assists = document.getElementById('nba-assists').value;
            payload.shooting_percentage = document.getElementById('nba-shooting').value;
        }
        
        // Swap panels: Show Result Card, hide Awaiting Placeholder
        placeholderCard.classList.add('hidden');
        resultCard.classList.remove('hidden');
        
        // Show spinner overlay
        resultSpinner.classList.remove('hidden');
        resultContent.classList.add('hidden');
        
        // Trigger API fetch
        fetch('/api/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        })
        .then(res => res.json())
        .then(data => {
            // Hide spinner overlay with small delay for transition feel
            setTimeout(() => {
                resultSpinner.classList.add('hidden');
                resultContent.classList.remove('hidden');
                
                if (data.error) {
                    alert(data.error);
                    placeholderCard.classList.remove('hidden');
                    resultCard.classList.add('hidden');
                    return;
                }
                
                // 1. Update winner card
                resultWinnerTeam.textContent = data.predicted_winner;
                resultWinProb.textContent = `${data.win_probability}%`;
                setRadialProbability(data.win_probability);
                
                // 2. Update expected score
                const details = data.expected_details;
                scoreTeam1Name.textContent = getAbbreviation(data.team1);
                scoreTeam2Name.textContent = getAbbreviation(data.team2);
                scoreTeam1Val.textContent = details.team1_val;
                scoreTeam2Val.textContent = details.team2_val;
                resultScoreText.textContent = data.expected_score;
                
                // Update score label depending on type
                document.getElementById('score-val-label').textContent = details.label;
                
                // 3. Update model info
                resultModelName.textContent = data.model_name;
                resultModelAcc.textContent = `${data.model_accuracy}%`;
                
                // 4. Update recent matches table
                resultHistoryRows.innerHTML = '';
                if (data.history && data.history.length > 0) {
                    data.history.forEach(hist => {
                        const tr = document.createElement('tr');
                        
                        // Detail text
                        const tdDetail = document.createElement('td');
                        tdDetail.innerHTML = `<span class="text-secondary">${hist.team1} vs ${hist.team2}</span>`;
                        
                        // Result text
                        const tdWinner = document.createElement('td');
                        if (hist.winner === 'Draw') {
                            tdWinner.innerHTML = `<span class="text-muted">Draw</span>`;
                        } else {
                            tdWinner.innerHTML = `<span class="hist-winner">${hist.winner} won</span>`;
                        }
                        
                        // Score text
                        const tdScore = document.createElement('td');
                        tdScore.textContent = hist.score || `${hist.team1_runs}-${hist.team2_runs}`;
                        
                        tr.appendChild(tdDetail);
                        tr.appendChild(tdWinner);
                        tr.appendChild(tdScore);
                        resultHistoryRows.appendChild(tr);
                    });
                } else {
                    const tr = document.createElement('tr');
                    tr.innerHTML = '<td colspan="3" class="text-center text-muted">No historical head-to-head matches found.</td>';
                    resultHistoryRows.appendChild(tr);
                }
            }, 600); // 600ms artificial delay to look professional
        })
        .catch(err => {
            resultSpinner.classList.add('hidden');
            console.error("Prediction failed:", err);
            alert("An error occurred while calculating prediction. Check server log.");
            placeholderCard.classList.remove('hidden');
            resultCard.classList.add('hidden');
        });
    });

    // Helper to abbreviate team names for score graphics
    function getAbbreviation(name) {
        if (!name) return '';
        // E.g., Chennai Super Kings -> CSK
        // Manchester United -> MNU (or split by spaces)
        const parts = name.split(' ');
        if (parts.length >= 3) {
            return parts.map(p => p[0]).join('').toUpperCase();
        } else if (parts.length === 2) {
            // E.g. Real Madrid -> RM
            return parts.map(p => p[0]).join('').toUpperCase();
        } else {
            // E.g. Barcelona -> BAR
            return name.substring(0, 3).toUpperCase();
        }
    }
});
