"""Ajustes de los ejemplos Python; conserva únicamente salidas compatibles."""
from pathlib import Path
import ast,json,re
from bs4 import BeautifulSoup
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
ROOT=Path(__file__).resolve().parents[1]
MASK_GUARD='''if mask is not None:
            mask = mask.to(device=keys.device, dtype=torch.bool)
            if mask.shape != keys.shape[:2] or not mask.any(dim=-1).all():
                raise ValueError("Cada secuencia debe tener al menos una clave válida")
            scores = scores.masked_fill(~mask, float("-inf"))'''
NMS='''def write_results(prediction, confidence, num_classes, nms_conf=0.4):
    """Filtra predicciones y aplica NMS por clase.

    Args:
        prediction: Tensor (batch, cajas, 5+clases), con centros y tamaños
            en píxeles y scores sigmoidales. No modifica este tensor.
        confidence: Umbral del producto objectness por score de clase.
        num_classes: Cantidad de clases de la salida.
        nms_conf: Umbral de IoU para suprimir duplicados de la misma clase.

    Returns:
        Tensor (detecciones, 8): batch, x1, y1, x2, y2, objectness,
        score de clase, índice de clase. Sin detecciones devuelve (0, 8).
    """
    rows = []
    for batch_index, image in enumerate(prediction):
        class_score, class_id = image[:, 5:5 + num_classes].max(dim=1)
        joint_score = image[:, 4] * class_score
        valid = joint_score > confidence
        image, class_score = image[valid], class_score[valid]
        class_id, joint_score = class_id[valid], joint_score[valid]
        if image.shape[0] == 0:
            continue
        # Convertir centro/tamaño a esquinas, conservando la entrada.
        boxes = torch.cat((image[:, :2] - image[:, 2:4] / 2,
                           image[:, :2] + image[:, 2:4] / 2), dim=1)
        for label in class_id.unique():
            candidates = torch.where(class_id == label)[0]
            order = candidates[joint_score[candidates].argsort(descending=True)]
            while order.numel():
                selected = order[0]
                rows.append(torch.cat((image.new_tensor([batch_index]),
                    boxes[selected], image[selected, 4:5],
                    class_score[selected:selected+1], label.to(image).reshape(1))))
                if order.numel() == 1:
                    break
                remaining = order[1:]
                iou = bbox_iou(boxes[selected].unsqueeze(0), boxes[remaining])
                order = remaining[iou <= nms_conf]
    return torch.stack(rows) if rows else prediction.new_empty((0, 8))
'''

def edit(code,file,cell):
    if file.startswith(('clase-02-','clase-03-','clase-04-')):
        code=code.replace('.squeeze()', '.squeeze(-1)')
    # Hace reproducible el índice del vocabulario independientemente del hash de Python.
    code=re.sub(r'list\(set\((tokens|vocabulary|words)\)\)',r'sorted(set(\1))',code)
    if 'mask = mask.to' not in code and 'scores.masked_fill(mask == 0, -1e9)' in code:
        code=code.replace('if mask is not None:\n            scores = scores.masked_fill(mask == 0, -1e9)',MASK_GUARD)
    if 'class LocalAttention' in code and '# 2. Predicción' in code:
        a=code.index('        # 2. Predicción');b=code.index('        context_vector =',a)
        code=code[:a]+'''        # Atenuación gaussiana global: variante suave con coste O(seq_len).
        valid = (torch.ones(keys.shape[:2], dtype=torch.bool, device=keys.device)
                 if mask is None else mask.to(device=keys.device, dtype=torch.bool))
        if valid.shape != keys.shape[:2] or not valid.any(dim=-1).all():
            raise ValueError("Cada secuencia debe tener al menos una clave válida")
        lengths = valid.sum(dim=-1).to(keys.dtype)
        p_t = (lengths - 1) * torch.sigmoid(self.vp(torch.tanh(self.wp(query)))).squeeze(-1)
        positions = torch.arange(seq_len, device=keys.device, dtype=keys.dtype)[None, :]
        sigma = max(self.window_size / 2.0, 1e-4)
        log_gaussian = -(positions - p_t[:, None]).square() / (2 * sigma**2)
        logits = (scores + log_gaussian).masked_fill(~valid, float("-inf"))
        attention_weights = F.softmax(logits, dim=-1)
'''+code[b:]
        code=code.replace('(Luong et al., 2015).','(variante didáctica inspirada en Luong et al., 2015).')
    if 'intra_mask = mask.unsqueeze(1) * mask.unsqueeze(2)' in code:
        code=code.replace('intra_mask = mask.unsqueeze(1) * mask.unsqueeze(2)\n            intra_scores = intra_scores.masked_fill(intra_mask == 0, -1e9)', '''valid = mask.to(device=keys.device, dtype=torch.bool)
            if valid.shape != keys.shape[:2] or not valid.any(dim=-1).all():
                raise ValueError("Cada secuencia debe tener al menos una clave válida")
            intra_scores = intra_scores.masked_fill(~valid[:, None, :], float("-inf"))''')
        target='''        # 2. Estados ocultos enriquecidos'''
        code=code.replace(target,'''        if mask is not None:
            intra_weights = intra_weights * valid[:, :, None]

'''+target)
        code=code.replace('Mecanismo de Intra-Attention / Auto-Alineación Interna (Cheng et al., 2016).','Autoatención bilineal didáctica; no reproduce la recurrencia LSTMN.')
    if 'last_hidden = h_n.squeeze(0)' in code and 'LSTM unidireccional con padding a la derecha:' not in code:
        code=code.replace('last_hidden = h_n.squeeze(0)', '''# LSTM unidireccional con padding a la derecha: consultar el último token válido.
        if mask is None:
            last_hidden = h_n.squeeze(0)
        else:
            valid = mask.to(device=x.device, dtype=torch.bool)
            lengths = valid.sum(dim=1)
            expected = torch.arange(x.size(1), device=x.device)[None, :] < lengths[:, None]
            if not lengths.gt(0).all() or not torch.equal(valid, expected):
                raise ValueError("Se requiere padding a la derecha y secuencias no vacías")
            last_hidden = lstm_out[torch.arange(x.size(0), device=x.device), lengths - 1]''')
    if file.startswith('clase-09-6-mecanismos-') and 'class AttentionLSTMClassifier' in code:
        code=code.replace('attention_type="bahdanau"','attention_type="decomposable"')
        code=code.replace('Módulos de Atención (Bahdanau, Luong, Local, Hard, Decomposable e Intra) definidos con éxito.', 'Módulos Decomposable e Intra definidos.')
    if file.startswith('clase-05-3-3-'):
        code=code.replace('if type(output) == int:', 'if output.numel() == 0:')
        code=code.replace('if type(detections) == int:', 'if detections.numel() == 0:')
        if 'def write_results(' in code:
            code=code[:code.index('def write_results(')]+NMS
            code=code.replace('inter_rect_x2 - inter_rect_x1 + 1','inter_rect_x2 - inter_rect_x1').replace('inter_rect_y2 - inter_rect_y1 + 1','inter_rect_y2 - inter_rect_y1')
            code=code.replace('b1_x2 - b1_x1 + 1','b1_x2 - b1_x1').replace('b1_y2 - b1_y1 + 1','b1_y2 - b1_y1')
            code=code.replace('b2_x2 - b2_x1 + 1','b2_x2 - b2_x1').replace('b2_y2 - b2_y1 + 1','b2_y2 - b2_y1')
            code=code.replace('inter_area / (b1_area + b2_area - inter_area)', 'inter_area / (b1_area + b2_area - inter_area).clamp_min(torch.finfo(inter_area.dtype).eps)')
        if code.lstrip().startswith('%%shell'):
            code='# En una celda de Colab/IPython:\n%pip install omegaconf configobj rich\n'
    # Los títulos gráficos describen el ejemplo, sin diagnosticar su señal real.
    replacements={
      'se pierden en negro':'tienen menor contraste en esta escala',
      'sólo formantes vocálicos son visibles':'algunas bandas tienen mayor contraste',
      'solo los formantes vocálicos son visibles':'algunas bandas tienen mayor contraste',
      'revela simultáneamente vocales y consonantes débiles':'comprime el rango de valores mostrado',
      'Entrada estándar para redes neuronales (Whisper, Conformer): 80 canales perceptuales comprimidos.':'Configuración del ejemplo: 80 bandas Mel; otros modelos pueden usar otra configuración.',
      '70%':'según el experimento',
    }
    for a,b in replacements.items():code=code.replace(a,b)
    return code

def run():
    report=[]
    for p in sorted((ROOT/'docs/nlp').glob('*.html')):
        s=BeautifulSoup(p.read_text(),'html.parser')
        for detail in list(s.select('details.source-code')):
            section=detail.find_parent('section');cell=section.get('id')
            pre=detail.find('pre');code=pre.get_text();new=edit(code,p.name,cell)
            if p.name.startswith('clase-04-') and cell=='celda-92':
                detail.decompose();continue
            if (p.name.startswith('clase-05-1-1-') and cell=='celda-85') or (p.name.startswith('clase-06-6-mecanismos-de-atencion-parte-1') and cell=='celda-83'):
                detail.decompose()
                para=s.new_tag('p')
                para.string=('Ejemplo NCHW: torch.randn(1, 3, 2, 2) representa una imagen de tres canales y espacio 2×2.' if cell=='celda-85' else 'El producto elemento a elemento de [0.01, 0.57, 0.9] y [0.723, 0.78, 0.41] es [0.00723, 0.4446, 0.369]. Es un ejemplo numérico de compuerta, no la sigmoide de [1,2,3].')
                section.append(para);continue
            if new!=code:
                pre.clear()
                fragment=BeautifulSoup('<pre>'+highlight(new,PythonLexer(),HtmlFormatter(nowrap=True))+'</pre>','html.parser').pre
                for n in list(fragment.contents):pre.append(n)
                for output in section.select('.output'):output.decompose()
                report.append({'page':str(p.relative_to(ROOT)),'cell':cell})
        for error in list(s.select('.saved-error')):error.decompose()
        p.write_text(str(s))
    (ROOT/'reports/codigo-vigente.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print('Celdas de código actualizadas:',len(report))
if __name__=='__main__':run()
