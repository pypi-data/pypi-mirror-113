Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var stacktrace_1 = require("app/types/stacktrace");
var CrashActions = function (_a) {
    var _b, _c;
    var stackView = _a.stackView, stackType = _a.stackType, stacktrace = _a.stacktrace, thread = _a.thread, exception = _a.exception, platform = _a.platform, onChange = _a.onChange;
    var hasSystemFrames = (stacktrace === null || stacktrace === void 0 ? void 0 : stacktrace.hasSystemFrames) ||
        !!((_b = exception === null || exception === void 0 ? void 0 : exception.values) === null || _b === void 0 ? void 0 : _b.find(function (value) { var _a; return !!((_a = value.stacktrace) === null || _a === void 0 ? void 0 : _a.hasSystemFrames); }));
    var hasMinified = !stackType
        ? false
        : !!((_c = exception === null || exception === void 0 ? void 0 : exception.values) === null || _c === void 0 ? void 0 : _c.find(function (value) { return value.rawStacktrace; })) || !!(thread === null || thread === void 0 ? void 0 : thread.rawStacktrace);
    var notify = function (options) {
        if (onChange) {
            onChange(options);
        }
    };
    var setStackType = function (type) { return function () {
        notify({ stackType: type });
    }; };
    var setStackView = function (view) { return function () {
        notify({ stackView: view });
    }; };
    var getOriginalButtonLabel = function () {
        if (platform === 'javascript' || platform === 'node') {
            return locale_1.t('Original');
        }
        return locale_1.t('Symbolicated');
    };
    var getMinifiedButtonLabel = function () {
        if (platform === 'javascript' || platform === 'node') {
            return locale_1.t('Minified');
        }
        return locale_1.t('Unsymbolicated');
    };
    return (<ButtonGroupWrapper>
      <buttonBar_1.default active={stackView} merged>
        {hasSystemFrames && (<button_1.default barId={stacktrace_1.STACK_VIEW.APP} size="xsmall" onClick={setStackView(stacktrace_1.STACK_VIEW.APP)}>
            {locale_1.t('App Only')}
          </button_1.default>)}
        <button_1.default barId={stacktrace_1.STACK_VIEW.FULL} size="xsmall" onClick={setStackView(stacktrace_1.STACK_VIEW.FULL)}>
          {locale_1.t('Full')}
        </button_1.default>
        <button_1.default barId={stacktrace_1.STACK_VIEW.RAW} onClick={setStackView(stacktrace_1.STACK_VIEW.RAW)} size="xsmall">
          {locale_1.t('Raw')}
        </button_1.default>
      </buttonBar_1.default>
      {hasMinified && (<buttonBar_1.default active={stackType} merged>
          <button_1.default barId={stacktrace_1.STACK_TYPE.ORIGINAL} size="xsmall" onClick={setStackType(stacktrace_1.STACK_TYPE.ORIGINAL)}>
            {getOriginalButtonLabel()}
          </button_1.default>
          <button_1.default barId={stacktrace_1.STACK_TYPE.MINIFIED} size="xsmall" onClick={setStackType(stacktrace_1.STACK_TYPE.MINIFIED)}>
            {getMinifiedButtonLabel()}
          </button_1.default>
        </buttonBar_1.default>)}
    </ButtonGroupWrapper>);
};
exports.default = CrashActions;
var ButtonGroupWrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-wrap: wrap;\n  > * {\n    padding: ", " 0;\n  }\n  > *:not(:last-child) {\n    margin-right: ", ";\n  }\n"], ["\n  display: flex;\n  flex-wrap: wrap;\n  > * {\n    padding: ", " 0;\n  }\n  > *:not(:last-child) {\n    margin-right: ", ";\n  }\n"])), space_1.default(0.5), space_1.default(1));
var templateObject_1;
//# sourceMappingURL=crashActions.jsx.map