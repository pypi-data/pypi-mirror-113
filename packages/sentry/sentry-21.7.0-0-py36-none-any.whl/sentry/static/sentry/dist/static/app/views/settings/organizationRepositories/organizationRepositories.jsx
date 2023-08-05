Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var alertLink_1 = tslib_1.__importDefault(require("app/components/alertLink"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var panels_1 = require("app/components/panels");
var repositoryRow_1 = tslib_1.__importDefault(require("app/components/repositoryRow"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var emptyMessage_1 = tslib_1.__importDefault(require("app/views/settings/components/emptyMessage"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var textBlock_1 = tslib_1.__importDefault(require("app/views/settings/components/text/textBlock"));
var OrganizationRepositories = function (_a) {
    var itemList = _a.itemList, onRepositoryChange = _a.onRepositoryChange, api = _a.api, params = _a.params;
    var orgId = params.orgId;
    var hasItemList = itemList && itemList.length > 0;
    return (<div>
      <settingsPageHeader_1.default title={locale_1.t('Repositories')}/>
      <alertLink_1.default to={"/settings/" + orgId + "/integrations/"}>
        {locale_1.t('Want to add a repository to start tracking commits? Install or configure your version control integration here.')}
      </alertLink_1.default>
      {!hasItemList && (<div className="m-b-2">
          <textBlock_1.default>
            {locale_1.t('Connecting a repository allows Sentry to capture commit data via webhooks. ' +
                'This enables features like suggested assignees and resolving issues via commit message. ' +
                "Once you've connected a repository, you can associate commits with releases via the API.")}
            &nbsp;
            {locale_1.tct('See our [link:documentation] for more details.', {
                link: <a href="https://docs.sentry.io/learn/releases/"/>,
            })}
          </textBlock_1.default>
        </div>)}

      {hasItemList ? (<panels_1.Panel>
          <panels_1.PanelHeader>{locale_1.t('Added Repositories')}</panels_1.PanelHeader>
          <panels_1.PanelBody>
            <div>
              {itemList.map(function (repo) { return (<repositoryRow_1.default key={repo.id} repository={repo} api={api} showProvider orgId={orgId} onRepositoryChange={onRepositoryChange}/>); })}
            </div>
          </panels_1.PanelBody>
        </panels_1.Panel>) : (<panels_1.Panel>
          <emptyMessage_1.default icon={<icons_1.IconCommit size="xl"/>} title={locale_1.t('Sentry is better with commit data')} description={locale_1.t('Adding one or more repositories will enable enhanced releases and the ability to resolve Sentry Issues via git message.')} action={<button_1.default href="https://docs.sentry.io/learn/releases/">
                {locale_1.t('Learn more')}
              </button_1.default>}/>
        </panels_1.Panel>)}
    </div>);
};
exports.default = OrganizationRepositories;
//# sourceMappingURL=organizationRepositories.jsx.map