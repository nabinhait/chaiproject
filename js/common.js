
// standard form actions
(function($) {
	// pass url and data in option
	$.fn.delete_table_row = function(opts) {
		this.delegate('button.delete-row-btn', 'click', function() {
			var $me = $(this);
			$me.attr('disabled',true).html('Deleting...');
			$.ajax({
				url: opts.url || 'lib/py/objstore.py',
				type: "DELETE",
				data: $.extend((opts.data || {}), 
					{name:$me.attr("data-name")}),
				success: function(data) {
					if(data.message=='ok') {
						$me.parent().parent().slideUp();			
					} else {
						alert(data.error);
						$me.attr('disabled',false).html('Delete');
					}
				}
			});
		});		
	}
})(jQuery)