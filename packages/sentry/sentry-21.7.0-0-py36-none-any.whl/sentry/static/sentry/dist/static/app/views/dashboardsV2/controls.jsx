Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var feature_1 = tslib_1.__importDefault(require("app/components/acl/feature"));
var featureDisabled_1 = tslib_1.__importDefault(require("app/components/acl/featureDisabled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var confirm_1 = tslib_1.__importDefault(require("app/components/confirm"));
var hovercard_1 = tslib_1.__importDefault(require("app/components/hovercard"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var types_1 = require("./types");
var Controls = /** @class */ (function (_super) {
    tslib_1.__extends(Controls, _super);
    function Controls() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Controls.prototype.render = function () {
        var _a = this.props, dashboardState = _a.dashboardState, dashboards = _a.dashboards, onEdit = _a.onEdit, onCancel = _a.onCancel, onCommit = _a.onCommit, onDelete = _a.onDelete;
        var cancelButton = (<button_1.default data-test-id="dashboard-cancel" onClick={function (e) {
                e.preventDefault();
                onCancel();
            }}>
        {locale_1.t('Cancel')}
      </button_1.default>);
        if ([types_1.DashboardState.EDIT, types_1.DashboardState.PENDING_DELETE].includes(dashboardState)) {
            return (<StyledButtonBar gap={1} key="edit-controls">
          {cancelButton}
          <confirm_1.default priority="danger" message={locale_1.t('Are you sure you want to delete this dashboard?')} onConfirm={onDelete} disabled={dashboards.length <= 1}>
            <button_1.default data-test-id="dashboard-delete" priority="danger">
              {locale_1.t('Delete')}
            </button_1.default>
          </confirm_1.default>
          <button_1.default data-test-id="dashboard-commit" onClick={function (e) {
                    e.preventDefault();
                    onCommit();
                }} priority="primary">
            {locale_1.t('Save and Finish')}
          </button_1.default>
        </StyledButtonBar>);
        }
        if (dashboardState === 'create') {
            return (<StyledButtonBar gap={1} key="create-controls">
          {cancelButton}
          <button_1.default data-test-id="dashboard-commit" onClick={function (e) {
                    e.preventDefault();
                    onCommit();
                }} priority="primary">
            {locale_1.t('Save and Finish')}
          </button_1.default>
        </StyledButtonBar>);
        }
        return (<StyledButtonBar gap={1} key="controls">
        <DashboardEditFeature>
          {function (hasFeature) { return (<button_1.default data-test-id="dashboard-edit" onClick={function (e) {
                    e.preventDefault();
                    onEdit();
                }} priority="primary" icon={<icons_1.IconEdit size="xs"/>} disabled={!hasFeature}>
              {locale_1.t('Edit Dashboard')}
            </button_1.default>); }}
        </DashboardEditFeature>
      </StyledButtonBar>);
    };
    return Controls;
}(React.Component));
var DashboardEditFeature = function (_a) {
    var children = _a.children;
    var noFeatureMessage = locale_1.t('Requires dashboard editing.');
    var renderDisabled = function (p) { return (<hovercard_1.default body={<featureDisabled_1.default features={p.features} hideHelpToggle message={noFeatureMessage} featureName={noFeatureMessage}/>}>
      {p.children(p)}
    </hovercard_1.default>); };
    return (<feature_1.default hookName="feature-disabled:dashboards-edit" features={['organizations:dashboards-edit']} renderDisabled={renderDisabled}>
      {function (_a) {
        var hasFeature = _a.hasFeature;
        return children(hasFeature);
    }}
    </feature_1.default>);
};
var StyledButtonBar = styled_1.default(buttonBar_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  @media (max-width: ", ") {\n    grid-auto-flow: row;\n    grid-row-gap: ", ";\n    width: 100%;\n  }\n"], ["\n  @media (max-width: ", ") {\n    grid-auto-flow: row;\n    grid-row-gap: ", ";\n    width: 100%;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; }, space_1.default(1));
exports.default = Controls;
var templateObject_1;
//# sourceMappingURL=controls.jsx.map