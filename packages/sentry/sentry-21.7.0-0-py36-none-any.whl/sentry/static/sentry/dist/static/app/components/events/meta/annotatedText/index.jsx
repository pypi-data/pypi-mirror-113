Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var capitalize_1 = tslib_1.__importDefault(require("lodash/capitalize"));
var list_1 = tslib_1.__importDefault(require("app/components/list"));
var listItem_1 = tslib_1.__importDefault(require("app/components/list/listItem"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var chunks_1 = tslib_1.__importDefault(require("./chunks"));
var utils_1 = require("./utils");
var valueElement_1 = tslib_1.__importDefault(require("./valueElement"));
var AnnotatedText = function (_a) {
    var value = _a.value, meta = _a.meta, props = tslib_1.__rest(_a, ["value", "meta"]);
    var renderValue = function () {
        var _a, _b;
        if (((_a = meta === null || meta === void 0 ? void 0 : meta.chunks) === null || _a === void 0 ? void 0 : _a.length) && meta.chunks.length > 1) {
            return <chunks_1.default chunks={meta.chunks}/>;
        }
        var element = <valueElement_1.default value={value} meta={meta}/>;
        if ((_b = meta === null || meta === void 0 ? void 0 : meta.rem) === null || _b === void 0 ? void 0 : _b.length) {
            var title = utils_1.getTooltipText({ rule_id: meta.rem[0][0], remark: meta.rem[0][1] });
            return <tooltip_1.default title={title}>{element}</tooltip_1.default>;
        }
        return element;
    };
    var formatErrorKind = function (kind) {
        return capitalize_1.default(kind.replace(/_/g, ' '));
    };
    var getErrorMessage = function (error) {
        var _a;
        var errorMessage = [];
        if (Array.isArray(error)) {
            if (error[0]) {
                errorMessage.push(formatErrorKind(error[0]));
            }
            if ((_a = error[1]) === null || _a === void 0 ? void 0 : _a.reason) {
                errorMessage.push("(" + error[1].reason + ")");
            }
        }
        else {
            errorMessage.push(formatErrorKind(error));
        }
        return errorMessage.join(' ');
    };
    var getTooltipTitle = function (errors) {
        if (errors.length === 1) {
            return <TooltipTitle>{locale_1.t('Error: %s', getErrorMessage(errors[0]))}</TooltipTitle>;
        }
        return (<TooltipTitle>
        <span>{locale_1.t('Errors:')}</span>
        <StyledList symbol="bullet">
          {errors.map(function (error, index) { return (<listItem_1.default key={index}>{getErrorMessage(error)}</listItem_1.default>); })}
        </StyledList>
      </TooltipTitle>);
    };
    var renderErrors = function (errors) {
        if (!errors.length) {
            return null;
        }
        return (<StyledTooltipError title={getTooltipTitle(errors)}>
        <StyledIconWarning color="red300"/>
      </StyledTooltipError>);
    };
    return (<span {...props}>
      {renderValue()}
      {(meta === null || meta === void 0 ? void 0 : meta.err) && renderErrors(meta.err)}
    </span>);
};
exports.default = AnnotatedText;
var StyledTooltipError = styled_1.default(tooltip_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-left: ", ";\n  vertical-align: middle;\n"], ["\n  margin-left: ", ";\n  vertical-align: middle;\n"])), space_1.default(0.75));
var StyledList = styled_1.default(list_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  li {\n    padding-left: ", ";\n    word-break: break-all;\n    :before {\n      border-color: ", ";\n      top: 6px;\n    }\n  }\n"], ["\n  li {\n    padding-left: ", ";\n    word-break: break-all;\n    :before {\n      border-color: ", ";\n      top: 6px;\n    }\n  }\n"])), space_1.default(3), function (p) { return p.theme.white; });
var TooltipTitle = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  text-align: left;\n"], ["\n  text-align: left;\n"])));
var StyledIconWarning = styled_1.default(icons_1.IconWarning)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  vertical-align: middle;\n"], ["\n  vertical-align: middle;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=index.jsx.map