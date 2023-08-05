Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var modal_1 = require("app/actionCreators/modal");
var actionLink_1 = tslib_1.__importDefault(require("app/components/actions/actionLink"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var customResolutionModal_1 = tslib_1.__importDefault(require("app/components/customResolutionModal"));
var dropdownLink_1 = tslib_1.__importDefault(require("app/components/dropdownLink"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var types_1 = require("app/types");
var analytics_1 = require("app/utils/analytics");
var formatters_1 = require("app/utils/formatters");
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var button_1 = tslib_1.__importDefault(require("./button"));
var menuHeader_1 = tslib_1.__importDefault(require("./menuHeader"));
var menuItemActionLink_1 = tslib_1.__importDefault(require("./menuItemActionLink"));
var defaultProps = {
    isResolved: false,
    isAutoResolved: false,
    confirmLabel: locale_1.t('Resolve'),
};
var ResolveActions = /** @class */ (function (_super) {
    tslib_1.__extends(ResolveActions, _super);
    function ResolveActions() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleCurrentReleaseResolution = function () {
            var _a = _this.props, onUpdate = _a.onUpdate, organization = _a.organization, hasRelease = _a.hasRelease, latestRelease = _a.latestRelease;
            hasRelease &&
                onUpdate({
                    status: types_1.ResolutionStatus.RESOLVED,
                    statusDetails: {
                        inRelease: latestRelease ? latestRelease.version : 'latest',
                    },
                });
            analytics_1.trackAnalyticsEvent({
                eventKey: 'resolve_issue',
                eventName: 'Resolve Issue',
                release: 'current',
                organization_id: organization.id,
            });
        };
        _this.handleNextReleaseResolution = function () {
            var _a = _this.props, onUpdate = _a.onUpdate, organization = _a.organization, hasRelease = _a.hasRelease;
            hasRelease &&
                onUpdate({
                    status: types_1.ResolutionStatus.RESOLVED,
                    statusDetails: {
                        inNextRelease: true,
                    },
                });
            analytics_1.trackAnalyticsEvent({
                eventKey: 'resolve_issue',
                eventName: 'Resolve Issue',
                release: 'next',
                organization_id: organization.id,
            });
        };
        return _this;
    }
    ResolveActions.prototype.handleAnotherExistingReleaseResolution = function (statusDetails) {
        var _a = this.props, organization = _a.organization, onUpdate = _a.onUpdate;
        onUpdate({
            status: types_1.ResolutionStatus.RESOLVED,
            statusDetails: statusDetails,
        });
        analytics_1.trackAnalyticsEvent({
            eventKey: 'resolve_issue',
            eventName: 'Resolve Issue',
            release: 'anotherExisting',
            organization_id: organization.id,
        });
    };
    ResolveActions.prototype.renderResolved = function () {
        var _a = this.props, isAutoResolved = _a.isAutoResolved, onUpdate = _a.onUpdate;
        return (<tooltip_1.default title={isAutoResolved
                ? locale_1.t('This event is resolved due to the Auto Resolve configuration for this project')
                : locale_1.t('Unresolve')}>
        <button_1.default priority="primary" icon={<icons_1.IconCheckmark size="xs"/>} label={locale_1.t('Unresolve')} disabled={isAutoResolved} onClick={function () { return onUpdate({ status: types_1.ResolutionStatus.UNRESOLVED }); }}/>
      </tooltip_1.default>);
    };
    ResolveActions.prototype.renderDropdownMenu = function () {
        var _this = this;
        var _a = this.props, projectSlug = _a.projectSlug, isResolved = _a.isResolved, hasRelease = _a.hasRelease, latestRelease = _a.latestRelease, confirmMessage = _a.confirmMessage, shouldConfirm = _a.shouldConfirm, disabled = _a.disabled, confirmLabel = _a.confirmLabel, disableDropdown = _a.disableDropdown;
        if (isResolved) {
            return this.renderResolved();
        }
        var actionTitle = !hasRelease
            ? locale_1.t('Set up release tracking in order to use this feature.')
            : '';
        var actionLinkProps = {
            shouldConfirm: shouldConfirm,
            message: confirmMessage,
            confirmLabel: confirmLabel,
            disabled: disabled || !hasRelease,
        };
        return (<dropdownLink_1.default customTitle={<button_1.default label={locale_1.t('More resolve options')} disabled={!projectSlug ? disabled : disableDropdown} icon={<icons_1.IconChevron direction="down" size="xs"/>}/>} caret={false} alwaysRenderMenu disabled={!projectSlug ? disabled : disableDropdown}>
        <menuHeader_1.default>{locale_1.t('Resolved In')}</menuHeader_1.default>

        <menuItemActionLink_1.default {...actionLinkProps} title={locale_1.t('The next release')} onAction={this.handleNextReleaseResolution}>
          <tooltip_1.default disabled={hasRelease} title={actionTitle}>
            {locale_1.t('The next release')}
          </tooltip_1.default>
        </menuItemActionLink_1.default>

        <menuItemActionLink_1.default {...actionLinkProps} title={locale_1.t('The current release')} onAction={this.handleCurrentReleaseResolution}>
          <tooltip_1.default disabled={hasRelease} title={actionTitle}>
            {latestRelease
                ? locale_1.t('The current release (%s)', formatters_1.formatVersion(latestRelease.version))
                : locale_1.t('The current release')}
          </tooltip_1.default>
        </menuItemActionLink_1.default>

        <menuItemActionLink_1.default {...actionLinkProps} title={locale_1.t('Another existing release')} onAction={function () { return hasRelease && _this.openCustomReleaseModal(); }} shouldConfirm={false}>
          <tooltip_1.default disabled={hasRelease} title={actionTitle}>
            {locale_1.t('Another existing release')}
          </tooltip_1.default>
        </menuItemActionLink_1.default>
      </dropdownLink_1.default>);
    };
    ResolveActions.prototype.openCustomReleaseModal = function () {
        var _this = this;
        var _a = this.props, orgSlug = _a.orgSlug, projectSlug = _a.projectSlug;
        modal_1.openModal(function (deps) { return (<customResolutionModal_1.default {...deps} onSelected={function (statusDetails) {
                return _this.handleAnotherExistingReleaseResolution(statusDetails);
            }} orgSlug={orgSlug} projectSlug={projectSlug}/>); });
    };
    ResolveActions.prototype.render = function () {
        var _a = this.props, isResolved = _a.isResolved, onUpdate = _a.onUpdate, confirmMessage = _a.confirmMessage, shouldConfirm = _a.shouldConfirm, disabled = _a.disabled, confirmLabel = _a.confirmLabel, projectFetchError = _a.projectFetchError;
        if (isResolved) {
            return this.renderResolved();
        }
        var actionLinkProps = {
            shouldConfirm: shouldConfirm,
            message: confirmMessage,
            confirmLabel: confirmLabel,
            disabled: disabled,
        };
        return (<tooltip_1.default disabled={!projectFetchError} title={locale_1.t('Error fetching project')}>
        <buttonBar_1.default merged>
          <actionLink_1.default {...actionLinkProps} type="button" title={locale_1.t('Resolve')} icon={<icons_1.IconCheckmark size="xs"/>} onAction={function () { return onUpdate({ status: types_1.ResolutionStatus.RESOLVED }); }}>
            {locale_1.t('Resolve')}
          </actionLink_1.default>
          {this.renderDropdownMenu()}
        </buttonBar_1.default>
      </tooltip_1.default>);
    };
    ResolveActions.defaultProps = defaultProps;
    return ResolveActions;
}(React.Component));
exports.default = withOrganization_1.default(ResolveActions);
//# sourceMappingURL=resolve.jsx.map