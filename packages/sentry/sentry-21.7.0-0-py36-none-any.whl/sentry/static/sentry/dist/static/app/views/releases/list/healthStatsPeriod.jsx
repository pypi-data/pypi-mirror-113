Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var types_1 = require("app/types");
var withGlobalSelection_1 = tslib_1.__importDefault(require("app/utils/withGlobalSelection"));
var HealthStatsPeriod = function (_a) {
    var _b;
    var location = _a.location, selection = _a.selection;
    var activePeriod = location.query.healthStatsPeriod || types_1.HealthStatsPeriodOption.TWENTY_FOUR_HOURS;
    var pathname = location.pathname, query = location.query;
    return (<Wrapper>
      {selection.datetime.period !== types_1.HealthStatsPeriodOption.TWENTY_FOUR_HOURS && (<Period to={{
                pathname: pathname,
                query: tslib_1.__assign(tslib_1.__assign({}, query), { healthStatsPeriod: types_1.HealthStatsPeriodOption.TWENTY_FOUR_HOURS }),
            }} selected={activePeriod === types_1.HealthStatsPeriodOption.TWENTY_FOUR_HOURS}>
          {locale_1.t('24h')}
        </Period>)}

      <Period to={{
            pathname: pathname,
            query: tslib_1.__assign(tslib_1.__assign({}, query), { healthStatsPeriod: types_1.HealthStatsPeriodOption.AUTO }),
        }} selected={activePeriod === types_1.HealthStatsPeriodOption.AUTO}>
        {selection.datetime.start ? locale_1.t('Custom') : (_b = selection.datetime.period) !== null && _b !== void 0 ? _b : locale_1.t('14d')}
      </Period>
    </Wrapper>);
};
var Wrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: column;\n  grid-column-gap: ", ";\n  flex: 1;\n  justify-content: flex-end;\n  text-align: right;\n  margin-left: ", ";\n"], ["\n  display: grid;\n  grid-auto-flow: column;\n  grid-column-gap: ", ";\n  flex: 1;\n  justify-content: flex-end;\n  text-align: right;\n  margin-left: ", ";\n"])), space_1.default(0.75), space_1.default(0.5));
var Period = styled_1.default(link_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n\n  &:hover,\n  &:focus {\n    color: ", ";\n  }\n"], ["\n  color: ", ";\n\n  &:hover,\n  &:focus {\n    color: ", ";\n  }\n"])), function (p) { return (p.selected ? p.theme.gray400 : p.theme.gray300); }, function (p) { return (p.selected ? p.theme.gray400 : p.theme.gray300); });
exports.default = withGlobalSelection_1.default(HealthStatsPeriod);
var templateObject_1, templateObject_2;
//# sourceMappingURL=healthStatsPeriod.jsx.map