Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var errorLevel_1 = tslib_1.__importDefault(require("app/components/events/errorLevel"));
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var EventMessage = function (_a) {
    var className = _a.className, level = _a.level, levelIndicatorSize = _a.levelIndicatorSize, message = _a.message, annotations = _a.annotations;
    return (<div className={className}>
    {level && (<StyledErrorLevel size={levelIndicatorSize} level={level}>
        {level}
      </StyledErrorLevel>)}

    {message && <Message>{message}</Message>}

    {annotations}
  </div>);
};
var StyledEventMessage = styled_1.default(EventMessage)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  position: relative;\n  line-height: 1.2;\n  overflow: hidden;\n"], ["\n  display: flex;\n  align-items: center;\n  position: relative;\n  line-height: 1.2;\n  overflow: hidden;\n"])));
var StyledErrorLevel = styled_1.default(errorLevel_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space_1.default(1));
var Message = styled_1.default('span')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  ", "\n  width: auto;\n  max-height: 38px;\n"], ["\n  ", "\n  width: auto;\n  max-height: 38px;\n"])), overflowEllipsis_1.default);
exports.default = StyledEventMessage;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=eventMessage.jsx.map