(function(window, document, undefined) {
    window.onload = function () {
        const tasksTable = document.querySelector('.tbl-task-list');
        tasksTable.addEventListener("click",  event => {
            const target = event.target;
            if (target.nodeName === 'BUTTON') {
                const url = target.dataset.url;
                const parent = target.parentElement;
                fetch(url, { method: 'post' })
                    .then(resp => resp.json())
                    .then(msg => {
                        console.log('Received message:', msg);
                        parent.removeChild(target);
                    });
            }
        });
    };
})(window, document);