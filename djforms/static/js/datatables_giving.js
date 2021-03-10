$(function(){
  /* datatables initialization for administrators */
  $('#data-table').DataTable({
    'lengthMenu': [
      [100, 200, 300],
      [100, 200, 300]
    ],
    'language': {
      'search': 'Filter records:',
      'processing': 'Loading...',
      'lengthMenu': 'Display _MENU_'
    },
    order: [[3, 'desc']],
    dom: 'lfrBtip',
    buttons: [
      {
        extend: 'excelHtml5',
        exportOptions: {
          columns: ':visible'
        }
      }
    ],
    //destroy: true,
    responsive: true,
    serverSide: true,
    processing: true,
    paging: true,
    pageLength: 100,
    ajax: {
       'url': $managerAjaxUrl,
       'type': 'post',
       'processData': true,
       'dataType': 'json',
       'data': {
            'csrfmiddlewaretoken': $csrfToken
       }
    },
    'columns': [
        {
            'data': 'last_name'
        },
        {
            'data': 'first_name',
            'searchable': false,
            'orderable': false
        },
        {
            'data': 'order_cc_name',
            'searchable': false,
            'orderable': false
        },
        {
            'data': 'created_at',
            'searchable': false
        },
        {
            'data': 'email',
            'searchable': false,
            'orderable': false
        },
        {
            'data': 'twitter'
        },
        {
            'data': 'phone',
            'searchable': false,
            'orderable': false
        },
        {
            'data': 'address',
            'searchable': false,
            'orderable': false
        },
        {
            'data': 'city'
        },
        {
            'data': 'state',
            'searchable': false
        },
        {
            'data': 'postal_code'
        },
        {
            'data': 'spouse',
            'searchable': false,
            'orderable': false
        },
        {
            'data': 'relation'
        },
        {
            'data': 'honouring',
            'searchable': false,
            'orderable': false
        },
        {
            'data': 'class_of',
            'searchable': false,
            'orderable': false
        },
        {
            'data': 'order_promo',
            'orderable': false,
            'searchable': false
        },
        {
            'data': 'order_transid',
            'orderable': false,
            'searchable': false
        },
        {
            'data': 'order_status',
            'searchable': false,
            'orderable': false
        },
        {
            'data': 'order_total',
            'searchable': false,
            'orderable': false
        },
        {
            'data': 'order_comments',
            'searchable': false,
            'orderable': false
        },
        {
            'data': 'anonymous',
            'searchable': false
        },
        {
            'data': 'hidden',
            'searchable': false
        }
    ]
  });
  console.log('done');
});
