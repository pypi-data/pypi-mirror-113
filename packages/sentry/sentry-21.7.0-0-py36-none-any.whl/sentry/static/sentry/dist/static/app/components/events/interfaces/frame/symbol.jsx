Object.defineProperty(exports, "__esModule", { value: true });
exports.FunctionNameToggleIcon = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var stacktracePreview_1 = require("app/components/stacktracePreview");
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("app/utils");
var functionName_1 = tslib_1.__importDefault(require("./functionName"));
var utils_2 = require("./utils");
var Symbol = function (_a) {
    var frame = _a.frame, onFunctionNameToggle = _a.onFunctionNameToggle, showCompleteFunctionName = _a.showCompleteFunctionName, isHoverPreviewed = _a.isHoverPreviewed;
    var hasFunctionNameHiddenDetails = utils_1.defined(frame.rawFunction) &&
        utils_1.defined(frame.function) &&
        frame.function !== frame.rawFunction;
    var getFunctionNameTooltipTitle = function () {
        if (!hasFunctionNameHiddenDetails) {
            return undefined;
        }
        if (!showCompleteFunctionName) {
            return locale_1.t('Expand function details');
        }
        return locale_1.t('Hide function details');
    };
    var _b = tslib_1.__read(utils_2.getFrameHint(frame), 2), hint = _b[0], hintIcon = _b[1];
    var enablePathTooltip = utils_1.defined(frame.absPath) && frame.absPath !== frame.filename;
    var functionNameTooltipTitle = getFunctionNameTooltipTitle();
    var tooltipDelay = isHoverPreviewed ? stacktracePreview_1.STACKTRACE_PREVIEW_TOOLTIP_DELAY : undefined;
    return (<Wrapper>
      <FunctionNameToggleTooltip title={functionNameTooltipTitle} containerDisplayMode="inline-flex" delay={tooltipDelay}>
        <FunctionNameToggleIcon hasFunctionNameHiddenDetails={hasFunctionNameHiddenDetails} onClick={hasFunctionNameHiddenDetails ? onFunctionNameToggle : undefined} size="xs" color="purple300"/>
      </FunctionNameToggleTooltip>
      <Data>
        <StyledFunctionName frame={frame} showCompleteFunctionName={showCompleteFunctionName} hasHiddenDetails={hasFunctionNameHiddenDetails}/>
        {hint && (<HintStatus>
            <tooltip_1.default title={hint} delay={tooltipDelay}>
              {hintIcon}
            </tooltip_1.default>
          </HintStatus>)}
        {frame.filename && (<FileNameTooltip title={frame.absPath} disabled={!enablePathTooltip} delay={tooltipDelay}>
            <Filename>
              {'('}
              {frame.filename}
              {frame.lineNo && ":" + frame.lineNo}
              {')'}
            </Filename>
          </FileNameTooltip>)}
      </Data>
    </Wrapper>);
};
var Wrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  text-align: left;\n  grid-column-start: 1;\n  grid-column-end: -1;\n  order: 3;\n  flex: 1;\n\n  display: flex;\n\n  code {\n    background: transparent;\n    color: ", ";\n    padding-right: ", ";\n  }\n\n  @media (min-width: ", ") {\n    order: 0;\n    grid-column-start: auto;\n    grid-column-end: auto;\n  }\n"], ["\n  text-align: left;\n  grid-column-start: 1;\n  grid-column-end: -1;\n  order: 3;\n  flex: 1;\n\n  display: flex;\n\n  code {\n    background: transparent;\n    color: ", ";\n    padding-right: ", ";\n  }\n\n  @media (min-width: ", ") {\n    order: 0;\n    grid-column-start: auto;\n    grid-column-end: auto;\n  }\n"])), function (p) { return p.theme.textColor; }, space_1.default(0.5), function (props) { return props.theme.breakpoints[0]; });
var StyledFunctionName = styled_1.default(functionName_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space_1.default(0.75));
var Data = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  max-width: 100%;\n"], ["\n  max-width: 100%;\n"])));
var HintStatus = styled_1.default('span')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  position: relative;\n  top: ", ";\n  margin: 0 ", " 0 -", ";\n"], ["\n  position: relative;\n  top: ", ";\n  margin: 0 ", " 0 -", ";\n"])), space_1.default(0.25), space_1.default(0.75), space_1.default(0.25));
var FileNameTooltip = styled_1.default(tooltip_1.default)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space_1.default(0.5));
var Filename = styled_1.default('span')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.purple300; });
var FunctionNameToggleIcon = styled_1.default(icons_1.IconFilter, {
    shouldForwardProp: function (prop) { return prop !== 'hasFunctionNameHiddenDetails'; },
})(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  cursor: pointer;\n  visibility: hidden;\n  display: none;\n  @media (min-width: ", ") {\n    display: block;\n  }\n  ", ";\n"], ["\n  cursor: pointer;\n  visibility: hidden;\n  display: none;\n  @media (min-width: ", ") {\n    display: block;\n  }\n  ", ";\n"])), function (p) { return p.theme.breakpoints[0]; }, function (p) { return !p.hasFunctionNameHiddenDetails && 'opacity: 0; cursor: inherit;'; });
exports.FunctionNameToggleIcon = FunctionNameToggleIcon;
var FunctionNameToggleTooltip = styled_1.default(tooltip_1.default)(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  height: 16px;\n  align-items: center;\n  margin-right: ", ";\n"], ["\n  height: 16px;\n  align-items: center;\n  margin-right: ", ";\n"])), space_1.default(0.75));
exports.default = Symbol;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8;
//# sourceMappingURL=symbol.jsx.map