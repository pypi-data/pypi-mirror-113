Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var omit_1 = tslib_1.__importDefault(require("lodash/omit"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var icons_1 = require("app/icons");
var SortLink = /** @class */ (function (_super) {
    tslib_1.__extends(SortLink, _super);
    function SortLink() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    SortLink.prototype.renderArrow = function () {
        var direction = this.props.direction;
        if (!direction) {
            return null;
        }
        if (direction === 'desc') {
            return <StyledIconArrow size="xs" direction="down"/>;
        }
        return <StyledIconArrow size="xs" direction="up"/>;
    };
    SortLink.prototype.render = function () {
        var _a = this.props, align = _a.align, title = _a.title, canSort = _a.canSort, generateSortLink = _a.generateSortLink, onClick = _a.onClick;
        var target = generateSortLink();
        if (!target || !canSort) {
            return <StyledNonLink align={align}>{title}</StyledNonLink>;
        }
        return (<StyledLink align={align} to={target} onClick={onClick}>
        {title} {this.renderArrow()}
      </StyledLink>);
    };
    return SortLink;
}(React.Component));
var StyledLink = styled_1.default(function (props) {
    var forwardProps = omit_1.default(props, ['align']);
    return <link_1.default {...forwardProps}/>;
})(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: block;\n  width: 100%;\n  white-space: nowrap;\n  color: inherit;\n\n  &:hover,\n  &:active,\n  &:focus,\n  &:visited {\n    color: inherit;\n  }\n\n  ", "\n"], ["\n  display: block;\n  width: 100%;\n  white-space: nowrap;\n  color: inherit;\n\n  &:hover,\n  &:active,\n  &:focus,\n  &:visited {\n    color: inherit;\n  }\n\n  ", "\n"])), function (p) { return (p.align ? "text-align: " + p.align + ";" : ''); });
var StyledNonLink = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: block;\n  width: 100%;\n  white-space: nowrap;\n  ", "\n"], ["\n  display: block;\n  width: 100%;\n  white-space: nowrap;\n  ", "\n"])), function (p) { return (p.align ? "text-align: " + p.align + ";" : ''); });
var StyledIconArrow = styled_1.default(icons_1.IconArrow)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  vertical-align: top;\n"], ["\n  vertical-align: top;\n"])));
exports.default = SortLink;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=sortLink.jsx.map