"use strict";

function hwaj() {
    var name = "";

    function set_name( n ) {
	name = n;
    }

    function get_name() {
	$.ajax( { 
	    url : 'http://localhost:8000/mp/hwaj/',
	    type : 'get',
	    data : { 'name' : name },
	    success : function ( data ) {
		//$('#greeting').text( data['response_data'] );
		$('#greeting').text( "fdsfkj" );
	    }
	} );
    }

    $("#submit_btn").click( function( event ) {
	event.preventDefault();
	var input_name = $("#name").val();
	set_name( input_name );
	get_name();
    } );
}

$( document ).ready( hwaj );
