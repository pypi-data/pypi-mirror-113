Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var editableText_1 = tslib_1.__importDefault(require("app/components/editableText"));
var locale_1 = require("app/locale");
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
function DashboardTitle(_a) {
    var dashboard = _a.dashboard, isEditing = _a.isEditing, organization = _a.organization, onUpdate = _a.onUpdate;
    return (<div>
      {!dashboard ? (locale_1.t('Dashboards')) : (<editableText_1.default isDisabled={!isEditing} value={organization.features.includes('dashboards-edit') &&
                dashboard.id === 'default-overview'
                ? 'Default Dashboard'
                : dashboard.title} onChange={function (newTitle) { return onUpdate(tslib_1.__assign(tslib_1.__assign({}, dashboard), { title: newTitle })); }} errorMessage={locale_1.t('Please set a title for this dashboard')} successMessage={locale_1.t('Dashboard title updated successfully')}/>)}
    </div>);
}
exports.default = withOrganization_1.default(DashboardTitle);
//# sourceMappingURL=title.jsx.map