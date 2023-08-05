Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var Sentry = tslib_1.__importStar(require("@sentry/react"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var dynamicSampling_1 = require("app/types/dynamicSampling");
var utils_1 = require("./utils");
function Conditions(_a) {
    var condition = _a.condition;
    function getConvertedValue(value) {
        if (Array.isArray(value)) {
            return (<react_1.Fragment>
          {tslib_1.__spreadArray([], tslib_1.__read(value)).map(function (v, index) { return (<react_1.Fragment key={v}>
              <Value>{v}</Value>
              {index !== value.length - 1 && <Separator>{'\u002C'}</Separator>}
            </react_1.Fragment>); })}
        </react_1.Fragment>);
        }
        return <Value>{String(value)}</Value>;
    }
    switch (condition.op) {
        case dynamicSampling_1.DynamicSamplingConditionOperator.AND: {
            var inner = condition.inner;
            if (!inner.length) {
                return <Label>{locale_1.t('All')}</Label>;
            }
            return (<Wrapper>
          {inner.map(function (_a, index) {
                    var value = _a.value, name = _a.name;
                    return (<div key={index}>
              <Label>{utils_1.getInnerNameLabel(name)}</Label>
              {getConvertedValue(value)}
            </div>);
                })}
        </Wrapper>);
        }
        default: {
            Sentry.captureException(new Error('Unknown dynamic sampling condition operator'));
            return null; // this shall not happen
        }
    }
}
exports.default = Conditions;
var Wrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n"])), space_1.default(1.5));
var Label = styled_1.default('span')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space_1.default(1));
var Value = styled_1.default('span')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  word-break: break-all;\n  white-space: pre-wrap;\n  color: ", ";\n"], ["\n  word-break: break-all;\n  white-space: pre-wrap;\n  color: ", ";\n"])), function (p) { return p.theme.gray300; });
var Separator = styled_1.default(Value)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  padding-right: ", ";\n"], ["\n  padding-right: ", ";\n"])), space_1.default(0.5));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=conditions.jsx.map