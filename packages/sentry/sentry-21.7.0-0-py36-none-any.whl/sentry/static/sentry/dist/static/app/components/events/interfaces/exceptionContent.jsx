Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var exceptionMechanism_1 = tslib_1.__importDefault(require("app/components/events/interfaces/exceptionMechanism"));
var annotated_1 = tslib_1.__importDefault(require("app/components/events/meta/annotated"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var stacktrace_1 = require("app/types/stacktrace");
var exceptionStacktraceContent_1 = tslib_1.__importDefault(require("./exceptionStacktraceContent"));
var exceptionTitle_1 = tslib_1.__importDefault(require("./exceptionTitle"));
var ExceptionContent = function (_a) {
    var newestFirst = _a.newestFirst, event = _a.event, stackView = _a.stackView, platform = _a.platform, values = _a.values, type = _a.type;
    if (!values) {
        return null;
    }
    var children = values.map(function (exc, excIdx) { return (<div key={excIdx} className="exception">
      <exceptionTitle_1.default type={exc.type} exceptionModule={exc === null || exc === void 0 ? void 0 : exc.module}/>
      <annotated_1.default object={exc} objectKey="value" required>
        {function (value) { return <StyledPre className="exc-message">{value}</StyledPre>; }}
      </annotated_1.default>
      {exc.mechanism && <exceptionMechanism_1.default data={exc.mechanism}/>}
      <exceptionStacktraceContent_1.default data={type === stacktrace_1.STACK_TYPE.ORIGINAL
            ? exc.stacktrace
            : exc.rawStacktrace || exc.stacktrace} stackView={stackView} stacktrace={exc.stacktrace} expandFirstFrame={excIdx === values.length - 1} platform={platform} newestFirst={newestFirst} event={event} chainedException={values.length > 1}/>
    </div>); });
    if (newestFirst) {
        children.reverse();
    }
    return <div>{children}</div>;
};
exports.default = ExceptionContent;
var StyledPre = styled_1.default('pre')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n  margin-top: 0;\n"], ["\n  margin-bottom: ", ";\n  margin-top: 0;\n"])), space_1.default(1));
var templateObject_1;
//# sourceMappingURL=exceptionContent.jsx.map