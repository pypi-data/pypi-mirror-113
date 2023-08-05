Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_document_title_1 = tslib_1.__importDefault(require("react-document-title"));
var panels_1 = require("app/components/panels");
var locale_1 = require("app/locale");
var apiChart_1 = tslib_1.__importDefault(require("./apiChart"));
var eventChart_1 = tslib_1.__importDefault(require("./eventChart"));
var AdminOverview = function () {
    var resolution = '1h';
    var since = new Date().getTime() / 1000 - 3600 * 24 * 7;
    return (<react_document_title_1.default title="Admin Overview - Sentry">
      <react_1.Fragment>
        <h3>{locale_1.t('System Overview')}</h3>

        <panels_1.Panel key="events">
          <panels_1.PanelHeader>{locale_1.t('Event Throughput')}</panels_1.PanelHeader>
          <panels_1.PanelBody withPadding>
            <eventChart_1.default since={since} resolution={resolution}/>
          </panels_1.PanelBody>
        </panels_1.Panel>

        <panels_1.Panel key="api">
          <panels_1.PanelHeader>{locale_1.t('API Responses')}</panels_1.PanelHeader>
          <panels_1.PanelBody withPadding>
            <apiChart_1.default since={since} resolution={resolution}/>
          </panels_1.PanelBody>
        </panels_1.Panel>
      </react_1.Fragment>
    </react_document_title_1.default>);
};
exports.default = AdminOverview;
//# sourceMappingURL=index.jsx.map