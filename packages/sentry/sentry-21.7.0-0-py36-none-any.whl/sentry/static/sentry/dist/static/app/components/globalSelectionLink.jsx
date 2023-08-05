Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_router_1 = require("react-router");
var qs = tslib_1.__importStar(require("query-string"));
var utils_1 = require("app/components/organizations/globalSelectionHeader/utils");
/**
 * A modified link used for navigating between organization level pages that
 * will keep the global selection values (projects, environments, time) in the
 * querystring when navigating if it's present
 *
 * Falls back to <a> if there is no router present.
 */
var GlobalSelectionLink = /** @class */ (function (_super) {
    tslib_1.__extends(GlobalSelectionLink, _super);
    function GlobalSelectionLink() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    GlobalSelectionLink.prototype.render = function () {
        var _a = this.props, location = _a.location, to = _a.to;
        var globalQuery = utils_1.extractSelectionParameters(location === null || location === void 0 ? void 0 : location.query);
        var hasGlobalQuery = Object.keys(globalQuery).length > 0;
        var query = typeof to === 'object' && to.query ? tslib_1.__assign(tslib_1.__assign({}, globalQuery), to.query) : globalQuery;
        if (location) {
            var toWithGlobalQuery = void 0;
            if (hasGlobalQuery) {
                if (typeof to === 'string') {
                    toWithGlobalQuery = { pathname: to, query: query };
                }
                else {
                    toWithGlobalQuery = tslib_1.__assign(tslib_1.__assign({}, to), { query: query });
                }
            }
            var routerProps = hasGlobalQuery
                ? tslib_1.__assign(tslib_1.__assign({}, this.props), { to: toWithGlobalQuery }) : tslib_1.__assign(tslib_1.__assign({}, this.props), { to: to });
            return <react_router_1.Link {...routerProps}>{this.props.children}</react_router_1.Link>;
        }
        else {
            var queryStringObject = {};
            if (typeof to === 'object' && to.search) {
                queryStringObject = qs.parse(to.search);
            }
            queryStringObject = tslib_1.__assign(tslib_1.__assign({}, queryStringObject), globalQuery);
            if (typeof to === 'object' && to.query) {
                queryStringObject = tslib_1.__assign(tslib_1.__assign({}, queryStringObject), to.query);
            }
            var url = (typeof to === 'string' ? to : to.pathname) +
                '?' +
                qs.stringify(queryStringObject);
            return (<a {...this.props} href={url}>
          {this.props.children}
        </a>);
        }
    };
    return GlobalSelectionLink;
}(React.Component));
exports.default = react_router_1.withRouter(GlobalSelectionLink);
//# sourceMappingURL=globalSelectionLink.jsx.map