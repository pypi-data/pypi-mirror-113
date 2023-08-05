Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var feature_1 = tslib_1.__importDefault(require("app/components/acl/feature"));
var featureDisabled_1 = tslib_1.__importDefault(require("app/components/acl/featureDisabled"));
var guideAnchor_1 = tslib_1.__importDefault(require("app/components/assistant/guideAnchor"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var dataExport_1 = tslib_1.__importStar(require("app/components/dataExport"));
var hovercard_1 = tslib_1.__importDefault(require("app/components/hovercard"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var analytics_1 = require("app/utils/analytics");
var utils_1 = require("../utils");
function handleDownloadAsCsv(title, _a) {
    var organization = _a.organization, eventView = _a.eventView, tableData = _a.tableData;
    analytics_1.trackAnalyticsEvent({
        eventKey: 'discover_v2.results.download_csv',
        eventName: 'Discoverv2: Download CSV',
        organization_id: parseInt(organization.id, 10),
    });
    utils_1.downloadAsCsv(tableData, eventView.getColumns(), title);
}
function renderDownloadButton(canEdit, props) {
    return (<feature_1.default features={['organizations:discover-query']} renderDisabled={function () { return renderBrowserExportButton(canEdit, props); }}>
      {renderAsyncExportButton(canEdit, props)}
    </feature_1.default>);
}
function renderBrowserExportButton(canEdit, props) {
    var isLoading = props.isLoading, error = props.error;
    var disabled = isLoading || error !== null || canEdit === false;
    var onClick = disabled ? undefined : function () { return handleDownloadAsCsv(props.title, props); };
    return (<button_1.default size="small" disabled={disabled} onClick={onClick} data-test-id="grid-download-csv" icon={<icons_1.IconDownload size="xs"/>}>
      {locale_1.t('Export')}
    </button_1.default>);
}
function renderAsyncExportButton(canEdit, props) {
    var isLoading = props.isLoading, error = props.error, location = props.location, eventView = props.eventView;
    var disabled = isLoading || error !== null || canEdit === false;
    return (<dataExport_1.default payload={{
            queryType: dataExport_1.ExportQueryType.Discover,
            queryInfo: eventView.getEventsAPIPayload(location),
        }} disabled={disabled} icon={<icons_1.IconDownload size="xs"/>}>
      {locale_1.t('Export All')}
    </dataExport_1.default>);
}
// Placate eslint proptype checking
function renderEditButton(canEdit, props) {
    var onClick = canEdit ? props.onEdit : undefined;
    return (<guideAnchor_1.default target="columns_header_button">
      <button_1.default size="small" disabled={!canEdit} onClick={onClick} data-test-id="grid-edit-enable" icon={<icons_1.IconStack size="xs"/>}>
        {locale_1.t('Columns')}
      </button_1.default>
    </guideAnchor_1.default>);
}
// Placate eslint proptype checking
function renderSummaryButton(_a) {
    var onChangeShowTags = _a.onChangeShowTags, showTags = _a.showTags;
    return (<button_1.default size="small" onClick={onChangeShowTags} icon={<icons_1.IconTag size="xs"/>}>
      {showTags ? locale_1.t('Hide Tags') : locale_1.t('Show Tags')}
    </button_1.default>);
}
function FeatureWrapper(props) {
    var noEditMessage = locale_1.t('Requires discover query feature.');
    var editFeatures = ['organizations:discover-query'];
    var renderDisabled = function (p) { return (<hovercard_1.default body={<featureDisabled_1.default features={p.features} hideHelpToggle message={noEditMessage} featureName={noEditMessage}/>}>
      {p.children(p)}
    </hovercard_1.default>); };
    return (<feature_1.default hookName="feature-disabled:grid-editable-actions" renderDisabled={renderDisabled} features={editFeatures}>
      {function (_a) {
        var hasFeature = _a.hasFeature;
        return props.children(hasFeature, props);
    }}
    </feature_1.default>);
}
function HeaderActions(props) {
    return (<React.Fragment>
      <FeatureWrapper {...props} key="edit">
        {renderEditButton}
      </FeatureWrapper>
      <FeatureWrapper {...props} key="download">
        {renderDownloadButton}
      </FeatureWrapper>
      {renderSummaryButton(props)}
    </React.Fragment>);
}
exports.default = HeaderActions;
//# sourceMappingURL=tableActions.jsx.map