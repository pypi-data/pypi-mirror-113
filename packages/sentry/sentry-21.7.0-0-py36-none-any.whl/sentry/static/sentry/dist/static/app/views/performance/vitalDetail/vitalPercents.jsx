Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var formatters_1 = require("app/utils/formatters");
var utils_1 = require("./utils");
function getVitalStateText(vital, vitalState) {
    switch (vitalState) {
        case utils_1.VitalState.POOR:
            return Array.isArray(vital)
                ? locale_1.t('Poor')
                : locale_1.tct('Poor: >[threshold]ms', { threshold: utils_1.webVitalPoor[vital] });
        case utils_1.VitalState.MEH:
            return Array.isArray(vital)
                ? locale_1.t('Meh')
                : locale_1.tct('Meh: >[threshold]ms', { threshold: utils_1.webVitalMeh[vital] });
        case utils_1.VitalState.GOOD:
            return Array.isArray(vital)
                ? locale_1.t('Good')
                : locale_1.tct('Good: <[threshold]ms', { threshold: utils_1.webVitalMeh[vital] });
        default:
            return null;
    }
}
function VitalPercents(props) {
    return (<VitalSet>
      {props.percents.map(function (pct) {
            return (<tooltip_1.default key={pct.vitalState} title={getVitalStateText(props.vital, pct.vitalState)}>
            <VitalStatus>
              {utils_1.vitalStateIcons[pct.vitalState]}
              <span>
                {props.showVitalPercentNames && locale_1.t("" + pct.vitalState)}{' '}
                {formatters_1.formatPercentage(pct.percent, 0)}
              </span>
            </VitalStatus>
          </tooltip_1.default>);
        })}
    </VitalSet>);
}
exports.default = VitalPercents;
var VitalSet = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: inline-grid;\n  grid-auto-flow: column;\n  gap: ", ";\n"], ["\n  display: inline-grid;\n  grid-auto-flow: column;\n  gap: ", ";\n"])), space_1.default(2));
var VitalStatus = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  gap: ", ";\n  font-size: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  gap: ", ";\n  font-size: ", ";\n"])), space_1.default(0.5), function (p) { return p.theme.fontSizeMedium; });
var templateObject_1, templateObject_2;
//# sourceMappingURL=vitalPercents.jsx.map