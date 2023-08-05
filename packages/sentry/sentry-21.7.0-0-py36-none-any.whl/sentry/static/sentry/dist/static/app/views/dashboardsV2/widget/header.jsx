Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var breadcrumbs_1 = tslib_1.__importDefault(require("app/components/breadcrumbs"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var confirm_1 = tslib_1.__importDefault(require("app/components/confirm"));
var editableText_1 = tslib_1.__importDefault(require("app/components/editableText"));
var Layout = tslib_1.__importStar(require("app/components/layouts/thirds"));
var locale_1 = require("app/locale");
function Header(_a) {
    var title = _a.title, orgSlug = _a.orgSlug, goBackLocation = _a.goBackLocation, dashboardTitle = _a.dashboardTitle, onChangeTitle = _a.onChangeTitle, onSave = _a.onSave, onDelete = _a.onDelete, isEditing = _a.isEditing;
    return (<Layout.Header>
      <Layout.HeaderContent>
        <breadcrumbs_1.default crumbs={[
            {
                to: "/organizations/" + orgSlug + "/dashboards/",
                label: locale_1.t('Dashboards'),
            },
            {
                to: goBackLocation,
                label: dashboardTitle,
            },
            { label: locale_1.t('Widget Builder') },
        ]}/>
        <Layout.Title>
          <editableText_1.default value={title} onChange={onChangeTitle} errorMessage={locale_1.t('Please set a title for this widget')} successMessage={locale_1.t('Widget title updated successfully')}/>
        </Layout.Title>
      </Layout.HeaderContent>

      <Layout.HeaderActions>
        <buttonBar_1.default gap={1}>
          <button_1.default title={locale_1.t("You’re seeing the metrics project because you have the feature flag 'organizations:metrics' enabled. Send us feedback via email.")} href="mailto:metrics-feedback@sentry.io?subject=Metrics Feedback">
            {locale_1.t('Give Feedback')}
          </button_1.default>
          <button_1.default to={goBackLocation}>{locale_1.t('Cancel')}</button_1.default>
          {isEditing && onDelete && (<confirm_1.default priority="danger" message={locale_1.t('Are you sure you want to delete this widget?')} onConfirm={onDelete}>
              <button_1.default priority="danger">{locale_1.t('Delete')}</button_1.default>
            </confirm_1.default>)}
          <button_1.default priority="primary" onClick={onSave} disabled={!onSave} title={!onSave ? locale_1.t('This feature is not yet available') : undefined}>
            {isEditing ? locale_1.t('Update Widget') : locale_1.t('Add Widget')}
          </button_1.default>
        </buttonBar_1.default>
      </Layout.HeaderActions>
    </Layout.Header>);
}
exports.default = Header;
//# sourceMappingURL=header.jsx.map