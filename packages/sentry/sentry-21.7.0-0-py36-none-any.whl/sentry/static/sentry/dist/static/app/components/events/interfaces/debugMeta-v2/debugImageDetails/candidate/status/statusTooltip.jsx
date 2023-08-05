Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("../utils");
var _1 = tslib_1.__importDefault(require("."));
function StatusTooltip(_a) {
    var candidate = _a.candidate, hasReprocessWarning = _a.hasReprocessWarning;
    var download = candidate.download;
    var _b = utils_1.getStatusTooltipDescription(candidate, hasReprocessWarning), label = _b.label, description = _b.description, disabled = _b.disabled;
    return (<tooltip_1.default title={label && (<Title>
            <Label>{label}</Label>
            {description && <div>{description}</div>}
          </Title>)} disabled={disabled}>
      <_1.default status={download.status}/>
    </tooltip_1.default>);
}
exports.default = StatusTooltip;
var Title = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  text-align: left;\n"], ["\n  text-align: left;\n"])));
var Label = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: inline-block;\n  margin-bottom: ", ";\n"], ["\n  display: inline-block;\n  margin-bottom: ", ";\n"])), space_1.default(0.25));
var templateObject_1, templateObject_2;
//# sourceMappingURL=statusTooltip.jsx.map