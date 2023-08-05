Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var debounce_1 = tslib_1.__importDefault(require("lodash/debounce"));
var integrations_1 = require("app/actionCreators/integrations");
var repositoryActions_1 = tslib_1.__importDefault(require("app/actions/repositoryActions"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var asyncComponent_1 = tslib_1.__importDefault(require("app/components/asyncComponent"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var dropdownAutoComplete_1 = tslib_1.__importDefault(require("app/components/dropdownAutoComplete"));
var dropdownButton_1 = tslib_1.__importDefault(require("app/components/dropdownButton"));
var pagination_1 = tslib_1.__importDefault(require("app/components/pagination"));
var panels_1 = require("app/components/panels");
var repositoryRow_1 = tslib_1.__importDefault(require("app/components/repositoryRow"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var emptyMessage_1 = tslib_1.__importDefault(require("app/views/settings/components/emptyMessage"));
var IntegrationRepos = /** @class */ (function (_super) {
    tslib_1.__extends(IntegrationRepos, _super);
    function IntegrationRepos() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        // Called by row to signal repository change.
        _this.onRepositoryChange = function (data) {
            var itemList = _this.state.itemList;
            itemList.forEach(function (item) {
                if (item.id === data.id) {
                    item.status = data.status;
                    // allow for custom scm repositories to be updated, and
                    // url is optional and therefore can be an empty string
                    item.url = data.url === undefined ? item.url : data.url;
                    item.name = data.name || item.name;
                }
            });
            _this.setState({ itemList: itemList });
            repositoryActions_1.default.resetRepositories();
        };
        _this.debouncedSearchRepositoriesRequest = debounce_1.default(function (query) { return _this.searchRepositoriesRequest(query); }, 200);
        _this.searchRepositoriesRequest = function (searchQuery) {
            var orgId = _this.props.organization.slug;
            var query = { search: searchQuery };
            var endpoint = "/organizations/" + orgId + "/integrations/" + _this.props.integration.id + "/repos/";
            return _this.api.request(endpoint, {
                method: 'GET',
                query: query,
                success: function (data) {
                    _this.setState({ integrationRepos: data, dropdownBusy: false });
                },
                error: function () {
                    _this.setState({ dropdownBusy: false });
                },
            });
        };
        _this.handleSearchRepositories = function (e) {
            _this.setState({ dropdownBusy: true });
            _this.debouncedSearchRepositoriesRequest(e.target.value);
        };
        return _this;
    }
    IntegrationRepos.prototype.getDefaultState = function () {
        return tslib_1.__assign(tslib_1.__assign({}, _super.prototype.getDefaultState.call(this)), { adding: false, itemList: [], integrationRepos: { repos: [], searchable: false }, dropdownBusy: false });
    };
    IntegrationRepos.prototype.getEndpoints = function () {
        var orgId = this.props.organization.slug;
        return [
            ['itemList', "/organizations/" + orgId + "/repos/", { query: { status: '' } }],
            [
                'integrationRepos',
                "/organizations/" + orgId + "/integrations/" + this.props.integration.id + "/repos/",
            ],
        ];
    };
    IntegrationRepos.prototype.getIntegrationRepos = function () {
        var integrationId = this.props.integration.id;
        return this.state.itemList.filter(function (repo) { return repo.integrationId === integrationId; });
    };
    IntegrationRepos.prototype.addRepo = function (selection) {
        var _this = this;
        var integration = this.props.integration;
        var itemList = this.state.itemList;
        var orgId = this.props.organization.slug;
        this.setState({ adding: true });
        var migratableRepo = itemList.filter(function (item) {
            if (!(selection.value && item.externalSlug)) {
                return false;
            }
            return selection.value === item.externalSlug;
        })[0];
        var promise;
        if (migratableRepo) {
            promise = integrations_1.migrateRepository(this.api, orgId, migratableRepo.id, integration);
        }
        else {
            promise = integrations_1.addRepository(this.api, orgId, selection.value, integration);
        }
        promise.then(function (repo) {
            _this.setState({ adding: false, itemList: itemList.concat(repo) });
            repositoryActions_1.default.resetRepositories();
        }, function () { return _this.setState({ adding: false }); });
    };
    IntegrationRepos.prototype.renderDropdown = function () {
        var _this = this;
        var access = new Set(this.props.organization.access);
        if (!access.has('org:integrations')) {
            return (<dropdownButton_1.default disabled title={locale_1.t('You must be an organization owner, manager or admin to add repositories')} isOpen={false} size="xsmall">
          {locale_1.t('Add Repository')}
        </dropdownButton_1.default>);
        }
        var repositories = new Set(this.state.itemList.filter(function (item) { return item.integrationId; }).map(function (i) { return i.externalSlug; }));
        var repositoryOptions = (this.state.integrationRepos.repos || []).filter(function (repo) { return !repositories.has(repo.identifier); });
        var items = repositoryOptions.map(function (repo) { return ({
            searchKey: repo.name,
            value: repo.identifier,
            label: (<StyledListElement>
          <StyledName>{repo.name}</StyledName>
        </StyledListElement>),
        }); });
        var menuHeader = <StyledReposLabel>{locale_1.t('Repositories')}</StyledReposLabel>;
        var onChange = this.state.integrationRepos.searchable
            ? this.handleSearchRepositories
            : undefined;
        return (<dropdownAutoComplete_1.default items={items} onSelect={this.addRepo.bind(this)} onChange={onChange} menuHeader={menuHeader} emptyMessage={locale_1.t('No repositories available')} noResultsMessage={locale_1.t('No repositories found')} busy={this.state.dropdownBusy} alignMenu="right">
        {function (_a) {
                var isOpen = _a.isOpen;
                return (<dropdownButton_1.default isOpen={isOpen} size="xsmall" busy={_this.state.adding}>
            {locale_1.t('Add Repository')}
          </dropdownButton_1.default>);
            }}
      </dropdownAutoComplete_1.default>);
    };
    IntegrationRepos.prototype.renderError = function (error) {
        var badRequest = Object.values(this.state.errors).find(function (resp) { return resp && resp.status === 400; });
        if (badRequest) {
            return (<alert_1.default type="error" icon={<icons_1.IconFlag size="md"/>}>
          {locale_1.t('We were unable to fetch repositories for this integration. Try again later, or reconnect this integration.')}
        </alert_1.default>);
        }
        return _super.prototype.renderError.call(this, error);
    };
    IntegrationRepos.prototype.renderBody = function () {
        var _this = this;
        var itemListPageLinks = this.state.itemListPageLinks;
        var orgId = this.props.organization.slug;
        var itemList = this.getIntegrationRepos() || [];
        var header = (<panels_1.PanelHeader disablePadding hasButtons>
        <HeaderText>{locale_1.t('Repositories')}</HeaderText>
        <DropdownWrapper>{this.renderDropdown()}</DropdownWrapper>
      </panels_1.PanelHeader>);
        return (<React.Fragment>
        <panels_1.Panel>
          {header}
          <panels_1.PanelBody>
            {itemList.length === 0 && (<emptyMessage_1.default icon={<icons_1.IconCommit />} title={locale_1.t('Sentry is better with commit data')} description={locale_1.t('Add a repository to begin tracking its commit data. Then, set up release tracking to unlock features like suspect commits, suggested issue owners, and deploy emails.')} action={<button_1.default href="https://docs.sentry.io/product/releases/">
                    {locale_1.t('Learn More')}
                  </button_1.default>}/>)}
            {itemList.map(function (repo) { return (<repositoryRow_1.default key={repo.id} repository={repo} orgId={orgId} api={_this.api} onRepositoryChange={_this.onRepositoryChange}/>); })}
          </panels_1.PanelBody>
        </panels_1.Panel>
        {itemListPageLinks && (<pagination_1.default pageLinks={itemListPageLinks} {...this.props}/>)}
      </React.Fragment>);
    };
    return IntegrationRepos;
}(asyncComponent_1.default));
exports.default = withOrganization_1.default(IntegrationRepos);
var HeaderText = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  padding-left: ", ";\n  flex: 1;\n"], ["\n  padding-left: ", ";\n  flex: 1;\n"])), space_1.default(2));
var DropdownWrapper = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  padding-right: ", ";\n  text-transform: none;\n"], ["\n  padding-right: ", ";\n  text-transform: none;\n"])), space_1.default(1));
var StyledReposLabel = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  width: 250px;\n  font-size: 0.875em;\n  padding: ", " 0;\n  text-transform: uppercase;\n"], ["\n  width: 250px;\n  font-size: 0.875em;\n  padding: ", " 0;\n  text-transform: uppercase;\n"])), space_1.default(1));
var StyledListElement = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  padding: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  padding: ", ";\n"])), space_1.default(0.5));
var StyledName = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  flex-shrink: 1;\n  min-width: 0;\n  ", ";\n"], ["\n  flex-shrink: 1;\n  min-width: 0;\n  ", ";\n"])), overflowEllipsis_1.default);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=integrationRepos.jsx.map