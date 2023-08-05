Object.defineProperty(exports, "__esModule", { value: true });
exports.attachTo = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_dom_1 = tslib_1.__importDefault(require("react-dom"));
var react_2 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var throttle_1 = tslib_1.__importDefault(require("lodash/throttle"));
var zxcvbn_1 = tslib_1.__importDefault(require("zxcvbn"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var theme_1 = tslib_1.__importDefault(require("app/utils/theme"));
/**
 * NOTE: Do not import this component synchronously. The zxcvbn library is
 * relatively large. This component should be loaded async as a split chunk.
 */
/**
 * The maximum score that zxcvbn reports
 */
var MAX_SCORE = 5;
var PasswordStrength = function (_a) {
    var value = _a.value, _b = _a.labels, labels = _b === void 0 ? ['Very Weak', 'Very Weak', 'Weak', 'Strong', 'Very Strong'] : _b, _c = _a.colors, colors = _c === void 0 ? [theme_1.default.red300, theme_1.default.red300, theme_1.default.yellow300, theme_1.default.green300, theme_1.default.green300] : _c;
    if (value === '') {
        return null;
    }
    var result = zxcvbn_1.default(value);
    if (!result) {
        return null;
    }
    var score = result.score;
    var percent = Math.round(((score + 1) / MAX_SCORE) * 100);
    var styles = react_2.css(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n    background: ", ";\n    width: ", "%;\n  "], ["\n    background: ", ";\n    width: ", "%;\n  "])), colors[score], percent);
    return (<react_1.Fragment>
      <StrengthProgress role="progressbar" aria-valuenow={score} aria-valuemin={0} aria-valuemax={100}>
        <StrengthProgressBar css={styles}/>
      </StrengthProgress>
      <StrengthLabel>
        {locale_1.tct('Strength: [textScore]', {
            textScore: <ScoreText>{labels[score]}</ScoreText>,
        })}
      </StrengthLabel>
    </react_1.Fragment>);
};
var StrengthProgress = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  background: ", ";\n  height: 8px;\n  border-radius: 2px;\n  overflow: hidden;\n"], ["\n  background: ", ";\n  height: 8px;\n  border-radius: 2px;\n  overflow: hidden;\n"])), theme_1.default.gray200);
var StrengthProgressBar = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  height: 100%;\n"], ["\n  height: 100%;\n"])));
var StrengthLabel = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  font-size: 0.8em;\n  margin-top: ", ";\n  color: ", ";\n"], ["\n  font-size: 0.8em;\n  margin-top: ", ";\n  color: ", ";\n"])), space_1.default(0.25), theme_1.default.gray400);
var ScoreText = styled_1.default('strong')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.black; });
exports.default = PasswordStrength;
/**
 * This is a shim that allows the password strength component to be used
 * outside of our main react application. Mostly useful since all of our
 * registration pages aren't in the react app.
 */
var attachTo = function (_a) {
    var input = _a.input, element = _a.element;
    return element &&
        input &&
        input.addEventListener('input', throttle_1.default(function (e) {
            react_dom_1.default.render(<PasswordStrength value={e.target.value}/>, element);
        }));
};
exports.attachTo = attachTo;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=passwordStrength.jsx.map