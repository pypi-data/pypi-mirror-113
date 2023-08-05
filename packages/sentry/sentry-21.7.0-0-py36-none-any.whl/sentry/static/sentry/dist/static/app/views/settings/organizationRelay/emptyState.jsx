Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var panels_1 = require("app/components/panels");
var locale_1 = require("app/locale");
var emptyMessage_1 = tslib_1.__importDefault(require("app/views/settings/components/emptyMessage"));
var EmptyState = function () { return (<panels_1.Panel>
    <emptyMessage_1.default>{locale_1.t('No Keys Registered.')}</emptyMessage_1.default>
  </panels_1.Panel>); };
exports.default = EmptyState;
//# sourceMappingURL=emptyState.jsx.map