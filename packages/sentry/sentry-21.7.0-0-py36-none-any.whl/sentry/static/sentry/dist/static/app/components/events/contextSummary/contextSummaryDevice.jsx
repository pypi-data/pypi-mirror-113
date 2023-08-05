Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var deviceName_1 = tslib_1.__importDefault(require("app/components/deviceName"));
var annotatedText_1 = tslib_1.__importDefault(require("app/components/events/meta/annotatedText"));
var metaProxy_1 = require("app/components/events/meta/metaProxy");
var textOverflow_1 = tslib_1.__importDefault(require("app/components/textOverflow"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var contextSummaryNoSummary_1 = tslib_1.__importDefault(require("./contextSummaryNoSummary"));
var generateClassName_1 = tslib_1.__importDefault(require("./generateClassName"));
var item_1 = tslib_1.__importDefault(require("./item"));
var ContextSummaryDevice = function (_a) {
    var data = _a.data;
    if (Object.keys(data).length === 0) {
        return <contextSummaryNoSummary_1.default title={locale_1.t('Unknown Device')}/>;
    }
    var renderName = function () {
        if (!data.model) {
            return locale_1.t('Unknown Device');
        }
        var meta = metaProxy_1.getMeta(data, 'model');
        return (<deviceName_1.default value={data.model}>
        {function (deviceName) {
                return <annotatedText_1.default value={deviceName} meta={meta}/>;
            }}
      </deviceName_1.default>);
    };
    var getSubTitle = function () {
        if (data.arch) {
            return {
                subject: locale_1.t('Arch:'),
                value: data.arch,
                meta: metaProxy_1.getMeta(data, 'arch'),
            };
        }
        if (data.model_id) {
            return {
                subject: locale_1.t('Model:'),
                value: data.model_id,
                meta: metaProxy_1.getMeta(data, 'model_id'),
            };
        }
        return null;
    };
    // TODO(dcramer): we need a better way to parse it
    var className = generateClassName_1.default(data.model);
    var subTitle = getSubTitle();
    return (<item_1.default className={className} icon={<span className="context-item-icon"/>}>
      <h3>{renderName()}</h3>
      {subTitle && (<textOverflow_1.default isParagraph>
          <Subject>{subTitle.subject}</Subject>
          <annotatedText_1.default value={subTitle.value} meta={subTitle.meta}/>
        </textOverflow_1.default>)}
    </item_1.default>);
};
exports.default = ContextSummaryDevice;
var Subject = styled_1.default('strong')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space_1.default(0.5));
var templateObject_1;
//# sourceMappingURL=contextSummaryDevice.jsx.map