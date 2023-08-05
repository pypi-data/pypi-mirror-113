Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var classnames_1 = tslib_1.__importDefault(require("classnames"));
var omit_1 = tslib_1.__importDefault(require("lodash/omit"));
var qs = tslib_1.__importStar(require("query-string"));
var ListLink = /** @class */ (function (_super) {
    tslib_1.__extends(ListLink, _super);
    function ListLink() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.getClassName = function () {
            var _classNames = {};
            var _a = _this.props, className = _a.className, activeClassName = _a.activeClassName;
            if (className) {
                _classNames[className] = true;
            }
            if (_this.isActive() && activeClassName) {
                _classNames[activeClassName] = true;
            }
            return classnames_1.default(_classNames);
        };
        return _this;
    }
    ListLink.prototype.isActive = function () {
        var _a = this.props, isActive = _a.isActive, to = _a.to, query = _a.query, index = _a.index, router = _a.router;
        var queryData = query ? qs.parse(query) : undefined;
        var target = typeof to === 'string' ? { pathname: to, query: queryData } : to;
        if (typeof isActive === 'function') {
            return isActive(target, index);
        }
        return router.isActive(target, index);
    };
    ListLink.prototype.render = function () {
        var _a = this.props, index = _a.index, children = _a.children, to = _a.to, disabled = _a.disabled, props = tslib_1.__rest(_a, ["index", "children", "to", "disabled"]);
        var carriedProps = omit_1.default(props, 'activeClassName', 'css', 'isActive', 'index', 'router', 'location');
        return (<StyledLi className={this.getClassName()} disabled={disabled}>
        <react_router_1.Link {...carriedProps} onlyActiveOnIndex={index} to={disabled ? '' : to}>
          {children}
        </react_router_1.Link>
      </StyledLi>);
    };
    ListLink.displayName = 'ListLink';
    ListLink.defaultProps = {
        activeClassName: 'active',
        index: false,
        disabled: false,
    };
    return ListLink;
}(React.Component));
exports.default = react_router_1.withRouter(ListLink);
var StyledLi = styled_1.default('li', {
    shouldForwardProp: function (prop) { return prop !== 'disabled'; },
})(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), function (p) {
    return p.disabled &&
        "\n   a {\n    color:" + p.theme.disabled + " !important;\n    pointer-events: none;\n    :hover {\n      color: " + p.theme.disabled + "  !important;\n    }\n   }\n";
});
var templateObject_1;
//# sourceMappingURL=listLink.jsx.map