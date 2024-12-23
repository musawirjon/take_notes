class MeetingWebSocket {
    constructor(meetingId, token) {
        this.ws = new WebSocket(`ws://your-api/ws/meeting/${meetingId}?token=${token}`);
        this.setupListeners();
    }

    setupListeners() {
        this.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            switch(data.type) {
                case 'transcription':
                    this.handleTranscription(data);
                    break;
                case 'note_update':
                    this.handleNoteUpdate(data);
                    break;
                case 'summary_update':
                    this.handleSummaryUpdate(data);
                    break;
            }
        };
    }

    handleTranscription(data) {
        // Update UI with new transcription
        const transcriptionDiv = document.getElementById('transcription');
        transcriptionDiv.innerHTML += `
            <p><strong>${data.speaker}:</strong> ${data.content}</p>
        `;
    }

    handleNoteUpdate(data) {
        // Update UI with new notes
        const notesDiv = document.getElementById('notes');
        notesDiv.innerHTML += `
            <div class="note">
                <p>${data.data.content}</p>
                <small>Added by ${data.data.user}</small>
            </div>
        `;
    }

    handleSummaryUpdate(data) {
        // Update UI with new summary
        const summaryDiv = document.getElementById('summary');
        summaryDiv.innerHTML = data.content;
    }
}

// Usage
const meeting = new MeetingWebSocket('meeting-id', 'user-token'); 