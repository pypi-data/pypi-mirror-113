Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var isEqual_1 = tslib_1.__importDefault(require("lodash/isEqual"));
var omit_1 = tslib_1.__importDefault(require("lodash/omit"));
var indicator_1 = require("app/actionCreators/indicator");
var modal_1 = require("app/actionCreators/modal");
var organizations_1 = require("app/actionCreators/organizations");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var textBlock_1 = tslib_1.__importDefault(require("app/views/settings/components/text/textBlock"));
var permissionAlert_1 = tslib_1.__importDefault(require("app/views/settings/organization/permissionAlert"));
var add_1 = tslib_1.__importDefault(require("./modals/add"));
var edit_1 = tslib_1.__importDefault(require("./modals/edit"));
var emptyState_1 = tslib_1.__importDefault(require("./emptyState"));
var list_1 = tslib_1.__importDefault(require("./list"));
var RELAY_DOCS_LINK = 'https://getsentry.github.io/relay/';
var RelayWrapper = /** @class */ (function (_super) {
    tslib_1.__extends(RelayWrapper, _super);
    function RelayWrapper() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleDelete = function (publicKey) { return function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var relays, trustedRelays, response, _a;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        relays = this.state.relays;
                        trustedRelays = relays
                            .filter(function (relay) { return relay.publicKey !== publicKey; })
                            .map(function (relay) { return omit_1.default(relay, ['created', 'lastModified']); });
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise("/organizations/" + this.props.organization.slug + "/", {
                                method: 'PUT',
                                data: { trustedRelays: trustedRelays },
                            })];
                    case 2:
                        response = _b.sent();
                        indicator_1.addSuccessMessage(locale_1.t('Successfully deleted Relay public key'));
                        this.setRelays(response.trustedRelays);
                        return [3 /*break*/, 4];
                    case 3:
                        _a = _b.sent();
                        indicator_1.addErrorMessage(locale_1.t('An unknown error occurred while deleting Relay public key'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); }; };
        _this.handleOpenEditDialog = function (publicKey) { return function () {
            var editRelay = _this.state.relays.find(function (relay) { return relay.publicKey === publicKey; });
            if (!editRelay) {
                return;
            }
            modal_1.openModal(function (modalProps) { return (<edit_1.default {...modalProps} savedRelays={_this.state.relays} api={_this.api} orgSlug={_this.props.organization.slug} relay={editRelay} onSubmitSuccess={function (response) {
                    _this.successfullySaved(response, locale_1.t('Successfully updated Relay public key'));
                }}/>); });
        }; };
        _this.handleOpenAddDialog = function () {
            modal_1.openModal(function (modalProps) { return (<add_1.default {...modalProps} savedRelays={_this.state.relays} api={_this.api} orgSlug={_this.props.organization.slug} onSubmitSuccess={function (response) {
                    _this.successfullySaved(response, locale_1.t('Successfully added Relay public key'));
                }}/>); });
        };
        _this.handleRefresh = function () {
            // Fetch fresh activities
            _this.fetchData();
        };
        return _this;
    }
    RelayWrapper.prototype.componentDidUpdate = function (prevProps, prevState) {
        if (!isEqual_1.default(prevState.relays, this.state.relays)) {
            // Fetch fresh activities
            this.fetchData();
            organizations_1.updateOrganization(tslib_1.__assign(tslib_1.__assign({}, prevProps.organization), { trustedRelays: this.state.relays }));
        }
        _super.prototype.componentDidUpdate.call(this, prevProps, prevState);
    };
    RelayWrapper.prototype.getTitle = function () {
        return locale_1.t('Relay');
    };
    RelayWrapper.prototype.getDefaultState = function () {
        return tslib_1.__assign(tslib_1.__assign({}, _super.prototype.getDefaultState.call(this)), { relays: this.props.organization.trustedRelays });
    };
    RelayWrapper.prototype.getEndpoints = function () {
        var organization = this.props.organization;
        return [['relayActivities', "/organizations/" + organization.slug + "/relay_usage/"]];
    };
    RelayWrapper.prototype.setRelays = function (trustedRelays) {
        this.setState({ relays: trustedRelays });
    };
    RelayWrapper.prototype.successfullySaved = function (response, successMessage) {
        indicator_1.addSuccessMessage(successMessage);
        this.setRelays(response.trustedRelays);
    };
    RelayWrapper.prototype.renderContent = function (disabled) {
        var _a = this.state, relays = _a.relays, relayActivities = _a.relayActivities, loading = _a.loading;
        if (loading) {
            return this.renderLoading();
        }
        if (!relays.length) {
            return <emptyState_1.default />;
        }
        return (<list_1.default relays={relays} relayActivities={relayActivities} onEdit={this.handleOpenEditDialog} onRefresh={this.handleRefresh} onDelete={this.handleDelete} disabled={disabled}/>);
    };
    RelayWrapper.prototype.renderBody = function () {
        var organization = this.props.organization;
        var disabled = !organization.access.includes('org:write');
        return (<react_1.Fragment>
        <settingsPageHeader_1.default title={locale_1.t('Relay')} action={<button_1.default title={disabled ? locale_1.t('You do not have permission to register keys') : undefined} priority="primary" size="small" icon={<icons_1.IconAdd size="xs" isCircled/>} onClick={this.handleOpenAddDialog} disabled={disabled}>
              {locale_1.t('Register Key')}
            </button_1.default>}/>
        <permissionAlert_1.default />
        <StyledTextBlock>
          {locale_1.t('Sentry Relay offers enterprise-grade data security by providing a standalone service that acts as a middle layer between your application and sentry.io.')}
        </StyledTextBlock>
        <textBlock_1.default>
          {locale_1.tct("Go to [link:Relay Documentation] for setup and details.", {
                link: <externalLink_1.default href={RELAY_DOCS_LINK}/>,
            })}
        </textBlock_1.default>
        {this.renderContent(disabled)}
      </react_1.Fragment>);
    };
    return RelayWrapper;
}(asyncView_1.default));
exports.default = RelayWrapper;
var StyledTextBlock = styled_1.default(textBlock_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  max-width: 600px;\n"], ["\n  max-width: 600px;\n"])));
var templateObject_1;
//# sourceMappingURL=relayWrapper.jsx.map