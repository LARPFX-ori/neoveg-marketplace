// Fades nos eventos selecionados: aplica fade de entrada e de saída de
// DURACAO_SEGUNDOS em cada evento selecionado (limitado a metade do evento).
// Licença: MIT OR Apache-2.0.

using System;
using ScriptPortal.Vegas;

public class EntryPoint
{
    // Altere aqui a duração dos fades.
    const double DURACAO_SEGUNDOS = 0.5;

    public void FromVegas(Vegas vegas)
    {
        foreach (Track trilha in vegas.Project.Tracks)
        {
            foreach (TrackEvent ev in trilha.Events)
            {
                if (!ev.Selected) continue;
                double ms = Math.Min(DURACAO_SEGUNDOS * 1000.0, ev.Length.Milliseconds / 2.0);
                if (ms <= 0) continue;
                ev.FadeIn.Length = Timecode.FromMilliseconds(ms);
                ev.FadeOut.Length = Timecode.FromMilliseconds(ms);
            }
        }
    }
}
