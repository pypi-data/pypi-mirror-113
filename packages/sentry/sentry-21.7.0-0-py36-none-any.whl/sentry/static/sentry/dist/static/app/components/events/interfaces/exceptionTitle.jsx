Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("app/utils");
var ExceptionTitle = function (_a) {
    var type = _a.type, exceptionModule = _a.exceptionModule;
    if (utils_1.defined(exceptionModule)) {
        return (<tooltip_1.default title={locale_1.tct('from [exceptionModule]', { exceptionModule: exceptionModule })}>
        <Title>{type}</Title>
      </tooltip_1.default>);
    }
    return <Title>{type}</Title>;
};
exports.default = ExceptionTitle;
var Title = styled_1.default('h5')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n  overflow-wrap: break-word;\n  word-wrap: break-word;\n  word-break: break-word;\n"], ["\n  margin-bottom: ", ";\n  overflow-wrap: break-word;\n  word-wrap: break-word;\n  word-break: break-word;\n"])), space_1.default(0.5));
var templateObject_1;
//# sourceMappingURL=exceptionTitle.jsx.map