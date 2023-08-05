Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var panels_1 = require("app/components/panels");
var locale_1 = require("app/locale");
var buildInSymbolSources_1 = tslib_1.__importDefault(require("./buildInSymbolSources"));
var symbolSources_1 = tslib_1.__importDefault(require("./symbolSources"));
function ExternalSources(_a) {
    var api = _a.api, organization = _a.organization, symbolSources = _a.symbolSources, builtinSymbolSources = _a.builtinSymbolSources, builtinSymbolSourceOptions = _a.builtinSymbolSourceOptions, projectSlug = _a.projectSlug, location = _a.location, router = _a.router;
    return (<panels_1.Panel>
      <panels_1.PanelHeader>{locale_1.t('External Sources')}</panels_1.PanelHeader>
      <panels_1.PanelBody>
        <symbolSources_1.default api={api} location={location} router={router} organization={organization} symbolSources={symbolSources} projectSlug={projectSlug}/>
        <buildInSymbolSources_1.default api={api} organization={organization} builtinSymbolSources={builtinSymbolSources} builtinSymbolSourceOptions={builtinSymbolSourceOptions} projectSlug={projectSlug}/>
      </panels_1.PanelBody>
    </panels_1.Panel>);
}
exports.default = ExternalSources;
//# sourceMappingURL=index.jsx.map