app_name = "trade_claims"
app_title = "Trade Claims"
app_publisher = "GFLA"
app_description = "Учёт претензий"
app_email = "denis.a.fedotov@gmail.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "trade_claims",
# 		"logo": "/assets/trade_claims/logo.png",
# 		"title": "Trade Claims",
# 		"route": "/trade_claims",
# 		"has_permission": "trade_claims.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/trade_claims/css/trade_claims.css"
app_include_js = ["/assets/trade_claims/js/home_redirect.js"]

# include js, css files in header of web template
# web_include_css = "/assets/trade_claims/css/trade_claims.css"
# web_include_js = "/assets/trade_claims/js/trade_claims.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "trade_claims/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "trade_claims/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# automatically load and sync documents of this doctype from downstream apps
# importable_doctypes = [doctype_1]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "trade_claims.utils.jinja_methods",
# 	"filters": "trade_claims.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "trade_claims.install.before_install"
# after_install = "trade_claims.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "trade_claims.uninstall.before_uninstall"
# after_uninstall = "trade_claims.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "trade_claims.utils.before_app_install"
# after_app_install = "trade_claims.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "trade_claims.utils.before_app_uninstall"
# after_app_uninstall = "trade_claims.utils.after_app_uninstall"

# Build
# ------------------
# To hook into the build process

# after_build = "trade_claims.build.after_build"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "trade_claims.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"trade_claims.tasks.all"
# 	],
# 	"daily": [
# 		"trade_claims.tasks.daily"
# 	],
# 	"hourly": [
# 		"trade_claims.tasks.hourly"
# 	],
# 	"weekly": [
# 		"trade_claims.tasks.weekly"
# 	],
# 	"monthly": [
# 		"trade_claims.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "trade_claims.install.before_tests"

# Extend DocType Class
# ------------------------------
#
# Specify custom mixins to extend the standard doctype controller.
# extend_doctype_class = {
# 	"Task": "trade_claims.custom.task.CustomTaskMixin"
# }

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "trade_claims.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "trade_claims.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["trade_claims.utils.before_request"]
# after_request = ["trade_claims.utils.after_request"]

# Job Events
# ----------
# before_job = ["trade_claims.utils.before_job"]
# after_job = ["trade_claims.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"trade_claims.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []

