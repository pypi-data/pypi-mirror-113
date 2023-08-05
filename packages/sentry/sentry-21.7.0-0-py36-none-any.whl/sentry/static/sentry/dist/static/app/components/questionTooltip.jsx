Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var icons_1 = require("app/icons");
var QuestionIconContainer = styled_1.default('span')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: inline-block;\n  height: ", ";\n  line-height: ", ";\n\n  & svg {\n    transition: 120ms color;\n    color: ", ";\n\n    &:hover {\n      color: ", ";\n    }\n  }\n"], ["\n  display: inline-block;\n  height: ", ";\n  line-height: ", ";\n\n  & svg {\n    transition: 120ms color;\n    color: ", ";\n\n    &:hover {\n      color: ", ";\n    }\n  }\n"])), function (p) { var _a; return (_a = p.theme.iconSizes[p.size]) !== null && _a !== void 0 ? _a : p.size; }, function (p) { var _a; return (_a = p.theme.iconSizes[p.size]) !== null && _a !== void 0 ? _a : p.size; }, function (p) { return p.theme.gray200; }, function (p) { return p.theme.gray300; });
function QuestionTooltip(_a) {
    var title = _a.title, size = _a.size, className = _a.className, tooltipProps = tslib_1.__rest(_a, ["title", "size", "className"]);
    return (<QuestionIconContainer size={size} className={className}>
      <tooltip_1.default title={title} {...tooltipProps}>
        <icons_1.IconQuestion size={size}/>
      </tooltip_1.default>
    </QuestionIconContainer>);
}
exports.default = QuestionTooltip;
var templateObject_1;
//# sourceMappingURL=questionTooltip.jsx.map