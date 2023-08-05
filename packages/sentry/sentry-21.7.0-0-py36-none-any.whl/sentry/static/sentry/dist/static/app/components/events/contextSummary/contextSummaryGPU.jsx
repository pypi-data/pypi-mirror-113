Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var annotatedText_1 = tslib_1.__importDefault(require("app/components/events/meta/annotatedText"));
var metaProxy_1 = require("app/components/events/meta/metaProxy");
var textOverflow_1 = tslib_1.__importDefault(require("app/components/textOverflow"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var contextSummaryNoSummary_1 = tslib_1.__importDefault(require("./contextSummaryNoSummary"));
var generateClassName_1 = tslib_1.__importDefault(require("./generateClassName"));
var item_1 = tslib_1.__importDefault(require("./item"));
var ContextSummaryGPU = function (_a) {
    var data = _a.data;
    if (Object.keys(data).length === 0 || !data.name) {
        return <contextSummaryNoSummary_1.default title={locale_1.t('Unknown GPU')}/>;
    }
    var renderName = function () {
        var meta = metaProxy_1.getMeta(data, 'name');
        return <annotatedText_1.default value={data.name} meta={meta}/>;
    };
    var className = generateClassName_1.default(data.name);
    var getVersionElement = function () {
        if (data.vendor_name) {
            className = generateClassName_1.default(data.vendor_name);
            return {
                subject: locale_1.t('Vendor:'),
                value: data.vendor_name,
                meta: metaProxy_1.getMeta(data, 'vendor_name'),
            };
        }
        return {
            subject: locale_1.t('Vendor:'),
            value: locale_1.t('Unknown'),
        };
    };
    var versionElement = getVersionElement();
    return (<item_1.default className={className} icon={<span className="context-item-icon"/>}>
      <h3>{renderName()}</h3>
      <textOverflow_1.default isParagraph>
        <Subject>{versionElement.subject}</Subject>
        <annotatedText_1.default value={versionElement.value} meta={versionElement.meta}/>
      </textOverflow_1.default>
    </item_1.default>);
};
exports.default = ContextSummaryGPU;
var Subject = styled_1.default('strong')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space_1.default(0.5));
var templateObject_1;
//# sourceMappingURL=contextSummaryGPU.jsx.map