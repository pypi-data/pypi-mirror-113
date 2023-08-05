Object.defineProperty(exports, "__esModule", { value: true });
exports.LightWeightOrganizationDetails = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var organizations_1 = require("app/actionCreators/organizations");
var alertActions_1 = tslib_1.__importDefault(require("app/actions/alertActions"));
var api_1 = require("app/api");
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var errorBoundary_1 = tslib_1.__importDefault(require("app/components/errorBoundary"));
var footer_1 = tslib_1.__importDefault(require("app/components/footer"));
var thirds_1 = require("app/components/layouts/thirds");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var getRouteStringFromRoutes_1 = tslib_1.__importDefault(require("app/utils/getRouteStringFromRoutes"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var organizationContext_1 = tslib_1.__importDefault(require("app/views/organizationContext"));
function DeletionInProgress(_a) {
    var organization = _a.organization;
    return (<thirds_1.Body>
      <thirds_1.Main>
        <alert_1.default type="warning" icon={<icons_1.IconWarning />}>
          {locale_1.tct('The [organization] organization is currently in the process of being deleted from Sentry.', {
            organization: <strong>{organization.slug}</strong>,
        })}
        </alert_1.default>
      </thirds_1.Main>
    </thirds_1.Body>);
}
var DeletionPending = /** @class */ (function (_super) {
    tslib_1.__extends(DeletionPending, _super);
    function DeletionPending() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = { submitInProgress: false };
        _this.api = new api_1.Client();
        _this.onRestore = function () {
            if (_this.state.submitInProgress) {
                return;
            }
            _this.setState({ submitInProgress: true });
            _this.api.request("/organizations/" + _this.props.organization.slug + "/", {
                method: 'PUT',
                data: { cancelDeletion: true },
                success: function () {
                    window.location.reload();
                },
                error: function () {
                    alertActions_1.default.addAlert({
                        message: 'We were unable to restore this organization. Please try again or contact support.',
                        type: 'error',
                    });
                    _this.setState({ submitInProgress: false });
                },
            });
        };
        return _this;
    }
    DeletionPending.prototype.componentWillUnmount = function () {
        this.api.clear();
    };
    DeletionPending.prototype.render = function () {
        var organization = this.props.organization;
        var access = new Set(organization.access);
        return (<thirds_1.Body>
        <thirds_1.Main>
          <h3>{locale_1.t('Deletion Scheduled')}</h3>
          <p>
            {locale_1.tct('The [organization] organization is currently scheduled for deletion.', {
                organization: <strong>{organization.slug}</strong>,
            })}
          </p>

          {access.has('org:admin') ? (<div>
              <p>
                {locale_1.t('Would you like to cancel this process and restore the organization back to the original state?')}
              </p>
              <p>
                <button_1.default priority="primary" onClick={this.onRestore} disabled={this.state.submitInProgress}>
                  {locale_1.t('Restore Organization')}
                </button_1.default>
              </p>
            </div>) : (<p>
              {locale_1.t('If this is a mistake, contact an organization owner and ask them to restore this organization.')}
            </p>)}
          <p>
            <small>
              {locale_1.t("Note: Restoration is available until the process begins. Once it does, there's no recovering the data that has been removed.")}
            </small>
          </p>
        </thirds_1.Main>
      </thirds_1.Body>);
    };
    return DeletionPending;
}(react_1.Component));
var OrganizationDetailsBody = withOrganization_1.default(function OrganizationDetailsBody(_a) {
    var _b;
    var children = _a.children, organization = _a.organization;
    var status = (_b = organization === null || organization === void 0 ? void 0 : organization.status) === null || _b === void 0 ? void 0 : _b.id;
    if (organization && status === 'pending_deletion') {
        return <DeletionPending organization={organization}/>;
    }
    if (organization && status === 'deletion_in_progress') {
        return <DeletionInProgress organization={organization}/>;
    }
    return (<react_1.Fragment>
      <errorBoundary_1.default>{children}</errorBoundary_1.default>
      <footer_1.default />
    </react_1.Fragment>);
});
var OrganizationDetails = /** @class */ (function (_super) {
    tslib_1.__extends(OrganizationDetails, _super);
    function OrganizationDetails() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    OrganizationDetails.prototype.componentDidMount = function () {
        var routes = this.props.routes;
        var isOldRoute = getRouteStringFromRoutes_1.default(routes) === '/:orgId/';
        if (isOldRoute) {
            react_router_1.browserHistory.replace("/organizations/" + this.props.params.orgId + "/");
        }
    };
    OrganizationDetails.prototype.componentDidUpdate = function (prevProps) {
        if (prevProps.params &&
            this.props.params &&
            prevProps.params.orgId !== this.props.params.orgId) {
            organizations_1.switchOrganization();
        }
    };
    OrganizationDetails.prototype.render = function () {
        return (<organizationContext_1.default includeSidebar useLastOrganization {...this.props}>
        <OrganizationDetailsBody {...this.props}>
          {this.props.children}
        </OrganizationDetailsBody>
      </organizationContext_1.default>);
    };
    return OrganizationDetails;
}(react_1.Component));
exports.default = OrganizationDetails;
function LightWeightOrganizationDetails(props) {
    return <OrganizationDetails detailed={false} {...props}/>;
}
exports.LightWeightOrganizationDetails = LightWeightOrganizationDetails;
//# sourceMappingURL=index.jsx.map