// front end JS functions



// Creates another field in the form when the button is pressed
$(function(){
    
    var more_fields = `
                    <p>
                        <label>KEYWORD</br> 
                            <select name="andor" id="andor">
                            <option value="and" id="and">AND</option>
                            <option value="or" id="or">OR</option>
                            <option value="not" id="not">NOT</option>
                        </select>

                        <input name="kw1" type="text" size="30" id="kw1"placeholder='e.g."Election"'></label>
                        
                        <select name="fields" id="fields">
                            <option value="all fields">All fields</option>
                            <option value="title">Title</option>
                            <option value="full text">Full Text</option>
                            <option value="tags">Tags</option>
                        </select>
                    </p>
                `;

    $('#add-search-field').on('click', (function (e) {
        e.preventDefault();
        console.log("clicked");
        $(".input-fields").append(more_fields);
    }));

});