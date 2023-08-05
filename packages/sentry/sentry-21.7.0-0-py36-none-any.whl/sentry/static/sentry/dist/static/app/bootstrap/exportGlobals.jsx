Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_dom_1 = tslib_1.__importDefault(require("react-dom"));
var Router = tslib_1.__importStar(require("react-router"));
var Sentry = tslib_1.__importStar(require("@sentry/react"));
var create_react_class_1 = tslib_1.__importDefault(require("create-react-class"));
var jquery_1 = tslib_1.__importDefault(require("jquery"));
var moment_1 = tslib_1.__importDefault(require("moment"));
var prop_types_1 = tslib_1.__importDefault(require("prop-types"));
var reflux_1 = tslib_1.__importDefault(require("reflux"));
var plugins_1 = tslib_1.__importDefault(require("app/plugins"));
var globals = {
    // The following globals are used in sentry-plugins webpack externals
    // configuration.
    PropTypes: prop_types_1.default,
    React: React,
    Reflux: reflux_1.default,
    Router: Router,
    Sentry: Sentry,
    moment: moment_1.default,
    ReactDOM: {
        findDOMNode: react_dom_1.default.findDOMNode,
        render: react_dom_1.default.render,
    },
    // jQuery is still exported to the window as some bootsrap functionality
    // and legacy plugins like youtrack make use of it.
    $: jquery_1.default,
    jQuery: jquery_1.default,
    // django templates make use of these globals
    createReactClass: create_react_class_1.default,
    SentryApp: {},
};
// The SentryApp global contains exported app modules for use in javascript
// modules that are not compiled with the sentry bundle.
var SentryApp = {
    // The following components are used in sentry-plugins.
    Form: require('app/components/forms/form').default,
    FormState: require('app/components/forms/index').FormState,
    LoadingIndicator: require('app/components/loadingIndicator').default,
    plugins: {
        add: plugins_1.default.add,
        addContext: plugins_1.default.addContext,
        BasePlugin: plugins_1.default.BasePlugin,
        DefaultIssuePlugin: plugins_1.default.DefaultIssuePlugin,
    },
    // The following components are used in legacy django HTML views
    ConfigStore: require('app/stores/configStore').default,
    HookStore: require('app/stores/hookStore').default,
    Modal: require('app/actionCreators/modal'),
    getModalPortal: require('app/utils/getModalPortal').default,
};
globals.SentryApp = SentryApp;
Object.keys(globals).forEach(function (name) { return (window[name] = globals[name]); });
exports.default = globals;
//# sourceMappingURL=exportGlobals.jsx.map