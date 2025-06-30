const users = {
    Alice:   {likes: ['adventure', 'sci-fi'], history: ['vid1']},
    Bob:     {likes: ['comedy', 'drama'], history: ['vid2', 'vid4']},
    Charlie: {likes: ['documentary'], history: ['vid3']},
    Diana:   {likes: ['romance', 'drama'], history: ['vid4']},
    Ethan:   {likes: ['education', 'documentary'], history: ['vid5', 'vid3']},
    Fiona:   {likes: ['adventure'], history: ['vid1']},
    George:  {likes: ['comedy'], history: ['vid2']},
    Hannah:  {likes: ['adventure', 'education'], history: ['vid5']},
    Ian:     {likes: ['drama', 'sci-fi'], history: ['vid1', 'vid4']},
    Jenny:   {likes: ['documentary', 'comedy'], history: ['vid3', 'vid2']}
};

function loadUserHistory(userId) {
    const raw = localStorage.getItem(`history_${userId}`);
    if (raw) {
        try {
            users[userId].history = JSON.parse(raw);
        } catch {
            users[userId].history = [];
        }
    }
}

function saveUserHistory(userId) {
    localStorage.setItem(`history_${userId}`,
        JSON.stringify(users[userId].history));
}

const videos = [
    {id: 'vid1', title: 'Adventure in Space', url: 'https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4', tags: ['adventure', 'sci-fi']},
    {id: 'vid2', title: 'Funny Times', url: 'https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4', tags: ['comedy']},
    {id: 'vid3', title: 'Nature Documentary', url: 'https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4', tags: ['documentary']},
    {id: 'vid4', title: 'Drama on Stage', url: 'https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4', tags: ['drama', 'romance']},
    {id: 'vid5', title: 'Science Facts', url: 'https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4', tags: ['education', 'documentary']}
];

function getQueryParam(name) {
    const params = new URLSearchParams(window.location.search);
    return params.get(name);
}

function buildVideoList() {
    const user = getQueryParam('user');
    loadUserHistory(user);
    const container = document.getElementById('video-list');
    videos.forEach(v => {
        const link = document.createElement('a');
        link.href = `watch.html?user=${user}&video=${v.id}`;
        link.textContent = v.title;
        const div = document.createElement('div');
        div.appendChild(link);
        container.appendChild(div);
    });
}

function loadVideo() {
    const videoId = getQueryParam('video');
    const userId = getQueryParam('user');
    loadUserHistory(userId);
    const video = videos.find(v => v.id === videoId);
    if (!video) return;
    const player = document.getElementById('player');
    player.src = video.url;
    document.getElementById('video-title').textContent = video.title;

    const recommendation = document.getElementById('recommendation');
    let recommendationShown = false;
    player.addEventListener('timeupdate', () => {
        if (player.currentTime > 10 && !recommendationShown) {
            recommendationShown = true;
            if (!users[userId].history.includes(video.id)) {
                users[userId].history.push(video.id);
                saveUserHistory(userId);
            }
            const rec = recommend(video, users[userId]);
            recommendation.innerHTML = `<strong>Recommended for you:</strong> ${rec.title}`;
            recommendation.classList.remove('hidden');
        }
    });
}

function recommend(currentVideo, user) {
    const historyTags = user.history
        .map(id => videos.find(v => v.id === id))
        .filter(Boolean)
        .flatMap(v => v.tags);

    let best = null;
    let bestScore = -1;
    videos.forEach(v => {
        if (v.id === currentVideo.id) return;
        let score = 0;
        v.tags.forEach(t => {
            if (user.likes.includes(t)) score += 2;
            if (historyTags.includes(t)) score += 1;
        });
        if (score > bestScore) {
            bestScore = score;
            best = v;
        }
    });
    return best || videos.find(v => v.id !== currentVideo.id);
}

if (document.getElementById('video-list')) {
    buildVideoList();
} else if (document.getElementById('player')) {
    loadVideo();
}
