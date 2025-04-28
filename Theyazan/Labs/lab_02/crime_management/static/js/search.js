$(document).ready(function () {
    $('#text-search-form').on('submit', function (e) {
        e.preventDefault();
        const query = $('#search-text').val();
        $.ajax({
            url: '/search/',
            method: 'GET',
            data: { q: query },
            success: function (data) {
                let resultsHtml = '<ul>';
                data.forEach(item => {
                    resultsHtml += `<li>${item.name} (ID: ${item.id})</li>`;
                });
                resultsHtml += '</ul>';
                $('#text-search-results').html(resultsHtml);
            },
            error: function () {
                $('#text-search-results').html('<p class="text-danger">حدث خطأ أثناء البحث.</p>');
            }
        });
    });
});