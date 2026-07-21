// Автопереход с пустого /app/desktop на воркспейс Trade Claims.
frappe.router.on('change', function() {
    var route = frappe.get_route_str();
    if (route === 'desktop' || route === '') {
        frappe.set_route('trade-claims');
    }
});
