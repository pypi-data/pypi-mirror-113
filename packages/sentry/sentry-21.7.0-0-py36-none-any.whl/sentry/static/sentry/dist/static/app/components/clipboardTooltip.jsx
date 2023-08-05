Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var clipboard_1 = tslib_1.__importDefault(require("app/components/clipboard"));
var textOverflow_1 = tslib_1.__importDefault(require("app/components/textOverflow"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var icons_1 = require("app/icons");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
function ClipboardTooltip(_a) {
    var title = _a.title, onSuccess = _a.onSuccess, props = tslib_1.__rest(_a, ["title", "onSuccess"]);
    return (<tooltip_1.default {...props} title={<TooltipClipboardWrapper onClick={function (event) {
                event.stopPropagation();
            }}>
          <textOverflow_1.default>{title}</textOverflow_1.default>
          <clipboard_1.default value={title} onSuccess={onSuccess}>
            <TooltipClipboardIconWrapper>
              <icons_1.IconCopy size="xs" color="white"/>
            </TooltipClipboardIconWrapper>
          </clipboard_1.default>
        </TooltipClipboardWrapper>} isHoverable/>);
}
exports.default = ClipboardTooltip;
var TooltipClipboardWrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: auto max-content;\n  align-items: center;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: auto max-content;\n  align-items: center;\n  grid-gap: ", ";\n"])), space_1.default(0.5));
var TooltipClipboardIconWrapper = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  position: relative;\n  bottom: -", ";\n  :hover {\n    cursor: pointer;\n  }\n"], ["\n  position: relative;\n  bottom: -", ";\n  :hover {\n    cursor: pointer;\n  }\n"])), space_1.default(0.25));
var templateObject_1, templateObject_2;
//# sourceMappingURL=clipboardTooltip.jsx.map