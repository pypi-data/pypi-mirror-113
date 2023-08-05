Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var icons_1 = require("app/icons");
var Divider = function (_a) {
    var isHover = _a.isHover, isLast = _a.isLast;
    return isLast ? null : (<StyledDivider>
      <StyledIconChevron direction={isHover ? 'down' : 'right'} size="14px"/>
    </StyledDivider>);
};
var StyledIconChevron = styled_1.default(icons_1.IconChevron)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: block;\n"], ["\n  display: block;\n"])));
var StyledDivider = styled_1.default('span')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: inline-block;\n  margin-left: 6px;\n  color: ", ";\n  position: relative;\n"], ["\n  display: inline-block;\n  margin-left: 6px;\n  color: ", ";\n  position: relative;\n"])), function (p) { return p.theme.gray200; });
exports.default = Divider;
var templateObject_1, templateObject_2;
//# sourceMappingURL=divider.jsx.map