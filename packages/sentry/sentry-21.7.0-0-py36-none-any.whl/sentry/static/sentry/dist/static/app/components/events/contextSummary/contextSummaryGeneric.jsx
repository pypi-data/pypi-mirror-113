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
var ContextSummaryGeneric = function (_a) {
    var data = _a.data, unknownTitle = _a.unknownTitle;
    if (Object.keys(data).length === 0) {
        return <contextSummaryNoSummary_1.default title={unknownTitle}/>;
    }
    var renderValue = function (key) {
        var meta = metaProxy_1.getMeta(data, key);
        return <annotatedText_1.default value={data[key]} meta={meta}/>;
    };
    var className = generateClassName_1.default(data.name, data.version);
    return (<item_1.default className={className} icon={<span className="context-item-icon"/>}>
      <h3>{renderValue('name')}</h3>
      <textOverflow_1.default isParagraph>
        <Subject>{locale_1.t('Version:')}</Subject>
        {!data.version ? locale_1.t('Unknown') : renderValue('version')}
      </textOverflow_1.default>
    </item_1.default>);
};
exports.default = ContextSummaryGeneric;
var Subject = styled_1.default('strong')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space_1.default(0.5));
var templateObject_1;
//# sourceMappingURL=contextSummaryGeneric.jsx.map