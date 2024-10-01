document.addEventListener('DOMContentLoaded', function() {
    const categoryField = document.getElementById('id_category');
    const subcategoryField = document.getElementById('id_subcategory');

    categoryField.addEventListener('change', function() {
        const categoryId = this.value;

        // Clear existing subcategory options
        subcategoryField.innerHTML = '';

        if (categoryId) {
            fetch(`/api/v1/sub-categories/?category_id=${categoryId}`)
                .then(response => response.json())
                .then(data => {
                    data.forEach(subcategory => {
                        const option = document.createElement('option');
                        option.value = subcategory.id;
                        option.textContent = subcategory.title;  // Adjust field name as necessary
                        subcategoryField.appendChild(option);
                    });
                });
        }
    });
});