Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_router_1 = require("react-router");
var is_prop_valid_1 = tslib_1.__importDefault(require("@emotion/is-prop-valid"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var Sentry = tslib_1.__importStar(require("@sentry/react"));
/**
 * A context-aware version of Link (from react-router) that falls
 * back to <a> if there is no router present
 */
var Link = /** @class */ (function (_super) {
    tslib_1.__extends(Link, _super);
    function Link() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Link.prototype.componentDidMount = function () {
        var isRouterPresent = this.props.location;
        if (!isRouterPresent) {
            Sentry.captureException(new Error('The link component was rendered without being wrapped by a <Router />'));
        }
    };
    Link.prototype.render = function () {
        var _a = this.props, disabled = _a.disabled, to = _a.to, ref = _a.ref, location = _a.location, props = tslib_1.__rest(_a, ["disabled", "to", "ref", "location"]);
        if (!disabled && location) {
            return <react_router_1.Link to={to} ref={ref} {...props}/>;
        }
        if (typeof to === 'string') {
            return <Anchor href={to} ref={ref} disabled={disabled} {...props}/>;
        }
        return <Anchor href="" ref={ref} {...props} disabled/>;
    };
    return Link;
}(React.Component));
exports.default = react_router_1.withRouter(Link);
var Anchor = styled_1.default('a', {
    shouldForwardProp: function (prop) {
        return typeof prop === 'string' && is_prop_valid_1.default(prop) && prop !== 'disabled';
    },
})(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), function (p) {
    return p.disabled &&
        "\n  color:" + p.theme.disabled + ";\n  pointer-events: none;\n  :hover {\n    color: " + p.theme.disabled + ";\n  }\n  ";
});
var templateObject_1;
//# sourceMappingURL=link.jsx.map