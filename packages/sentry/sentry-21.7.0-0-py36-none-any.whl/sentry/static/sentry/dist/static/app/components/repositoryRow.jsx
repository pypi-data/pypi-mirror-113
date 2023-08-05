Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var integrations_1 = require("app/actionCreators/integrations");
var modal_1 = require("app/actionCreators/modal");
var access_1 = tslib_1.__importDefault(require("app/components/acl/access"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var confirm_1 = tslib_1.__importDefault(require("app/components/confirm"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var panels_1 = require("app/components/panels");
var repositoryEditForm_1 = tslib_1.__importDefault(require("app/components/repositoryEditForm"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var types_1 = require("app/types");
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var RepositoryRow = /** @class */ (function (_super) {
    tslib_1.__extends(RepositoryRow, _super);
    function RepositoryRow() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.cancelDelete = function () {
            var _a = _this.props, api = _a.api, orgId = _a.orgId, repository = _a.repository, onRepositoryChange = _a.onRepositoryChange;
            integrations_1.cancelDeleteRepository(api, orgId, repository.id).then(function (data) {
                if (onRepositoryChange) {
                    onRepositoryChange(data);
                }
            }, function () { });
        };
        _this.deleteRepo = function () {
            var _a = _this.props, api = _a.api, orgId = _a.orgId, repository = _a.repository, onRepositoryChange = _a.onRepositoryChange;
            integrations_1.deleteRepository(api, orgId, repository.id).then(function (data) {
                if (onRepositoryChange) {
                    onRepositoryChange(data);
                }
            }, function () { });
        };
        _this.handleEditRepo = function (data) {
            var onRepositoryChange = _this.props.onRepositoryChange;
            if (onRepositoryChange) {
                onRepositoryChange(data);
            }
        };
        _this.openModal = function () {
            var _a = _this.props, repository = _a.repository, orgId = _a.orgId;
            modal_1.openModal(function (_a) {
                var Body = _a.Body, Header = _a.Header, closeModal = _a.closeModal;
                return (<react_1.Fragment>
        <Header closeButton>{locale_1.t('Edit Repository')}</Header>
        <Body>
          <repositoryEditForm_1.default orgSlug={orgId} repository={repository} onSubmitSuccess={_this.handleEditRepo} closeModal={closeModal} onCancel={closeModal}/>
        </Body>
      </react_1.Fragment>);
            });
        };
        return _this;
    }
    RepositoryRow.prototype.getStatusLabel = function (repo) {
        switch (repo.status) {
            case types_1.RepositoryStatus.PENDING_DELETION:
                return 'Deletion Queued';
            case types_1.RepositoryStatus.DELETION_IN_PROGRESS:
                return 'Deletion in Progress';
            case types_1.RepositoryStatus.DISABLED:
                return 'Disabled';
            case types_1.RepositoryStatus.HIDDEN:
                return 'Disabled';
            default:
                return null;
        }
    };
    Object.defineProperty(RepositoryRow.prototype, "isActive", {
        get: function () {
            return this.props.repository.status === types_1.RepositoryStatus.ACTIVE;
        },
        enumerable: false,
        configurable: true
    });
    RepositoryRow.prototype.renderDeleteButton = function (hasAccess) {
        var repository = this.props.repository;
        var isActive = this.isActive;
        return (<tooltip_1.default title={locale_1.t('You must be an organization owner, manager or admin to remove a repository.')} disabled={hasAccess}>
        <confirm_1.default disabled={!hasAccess || (!isActive && repository.status !== types_1.RepositoryStatus.DISABLED)} onConfirm={this.deleteRepo} message={locale_1.t('Are you sure you want to remove this repository? All associated commit data will be removed in addition to the repository.')}>
          <StyledButton size="xsmall" icon={<icons_1.IconDelete size="xs"/>} label={locale_1.t('delete')} disabled={!hasAccess}/>
        </confirm_1.default>
      </tooltip_1.default>);
    };
    RepositoryRow.prototype.render = function () {
        var _this = this;
        var _a = this.props, repository = _a.repository, showProvider = _a.showProvider, organization = _a.organization;
        var isActive = this.isActive;
        var isCustomRepo = organization.features.includes('integrations-custom-scm') &&
            repository.provider.id === 'integrations:custom_scm';
        return (<access_1.default access={['org:integrations']}>
        {function (_a) {
                var hasAccess = _a.hasAccess;
                return (<StyledPanelItem status={repository.status}>
            <RepositoryTitleAndUrl>
              <RepositoryTitle>
                <strong>{repository.name}</strong>
                {!isActive && <small> &mdash; {_this.getStatusLabel(repository)}</small>}
                {repository.status === types_1.RepositoryStatus.PENDING_DELETION && (<StyledButton size="xsmall" onClick={_this.cancelDelete} disabled={!hasAccess} data-test-id="repo-cancel">
                    {locale_1.t('Cancel')}
                  </StyledButton>)}
              </RepositoryTitle>
              <div>
                {showProvider && <small>{repository.provider.name}</small>}
                {showProvider && repository.url && <span>&nbsp;&mdash;&nbsp;</span>}
                {repository.url && (<small>
                    <externalLink_1.default href={repository.url}>
                      {repository.url.replace('https://', '')}
                    </externalLink_1.default>
                  </small>)}
              </div>
            </RepositoryTitleAndUrl>
            {isCustomRepo ? (<EditAndDelete>
                <StyledButton size="xsmall" icon={<icons_1.IconEdit size="xs"/>} label={locale_1.t('edit')} disabled={!hasAccess ||
                            (!isActive && repository.status !== types_1.RepositoryStatus.DISABLED)} onClick={function () { return _this.openModal(); }}/>
                {_this.renderDeleteButton(hasAccess)}
              </EditAndDelete>) : (_this.renderDeleteButton(hasAccess))}
          </StyledPanelItem>);
            }}
      </access_1.default>);
    };
    RepositoryRow.defaultProps = {
        showProvider: false,
    };
    return RepositoryRow;
}(react_1.Component));
var StyledPanelItem = styled_1.default(panels_1.PanelItem)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  /* shorter top padding because of title lineheight */\n  padding: ", " ", " ", ";\n  justify-content: space-between;\n  align-items: center;\n  flex: 1;\n\n  ", ";\n\n  &:last-child {\n    border-bottom: none;\n  }\n"], ["\n  /* shorter top padding because of title lineheight */\n  padding: ", " ", " ", ";\n  justify-content: space-between;\n  align-items: center;\n  flex: 1;\n\n  ", ";\n\n  &:last-child {\n    border-bottom: none;\n  }\n"])), space_1.default(1), space_1.default(2), space_1.default(2), function (p) {
    return p.status === types_1.RepositoryStatus.DISABLED &&
        "\n    filter: grayscale(1);\n    opacity: 0.4;\n  ";
});
var StyledButton = styled_1.default(button_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space_1.default(1));
var RepositoryTitleAndUrl = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n"], ["\n  display: flex;\n  flex-direction: column;\n"])));
var EditAndDelete = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  margin-left: ", ";\n"], ["\n  display: flex;\n  margin-left: ", ";\n"])), space_1.default(1));
var RepositoryTitle = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n  /* accommodate cancel button height */\n  line-height: 26px;\n"], ["\n  margin-bottom: ", ";\n  /* accommodate cancel button height */\n  line-height: 26px;\n"])), space_1.default(1));
exports.default = withOrganization_1.default(RepositoryRow);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=repositoryRow.jsx.map