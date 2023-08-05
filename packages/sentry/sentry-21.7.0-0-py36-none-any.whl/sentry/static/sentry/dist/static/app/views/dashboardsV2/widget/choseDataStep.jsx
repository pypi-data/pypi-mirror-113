Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var locale_1 = require("app/locale");
var radioField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/radioField"));
var buildStep_1 = tslib_1.__importDefault(require("./buildStep"));
var utils_1 = require("./utils");
var dataSetChoices = [
    [utils_1.DataSet.EVENTS, locale_1.t('Events')],
    [utils_1.DataSet.METRICS, locale_1.t('Metrics')],
];
function ChooseDataSetStep(_a) {
    var value = _a.value, onChange = _a.onChange;
    return (<buildStep_1.default title={locale_1.t('Choose your data set')} description={locale_1.t('Monitor specific events such as errors and transactions or get metric readings on TBD.')}>
      <radioField_1.default name="dataSet" onChange={onChange} value={value} choices={dataSetChoices} inline={false} orientInline hideControlState stacked/>
    </buildStep_1.default>);
}
exports.default = ChooseDataSetStep;
//# sourceMappingURL=choseDataStep.jsx.map